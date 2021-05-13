#!/usr/bin/env python

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from model.TeamDto import Team
from model.DriverDto import Driver


def search_driver_name(driver_id, drivers):
    for d in drivers:
        if d.id == driver_id:
            toret = d.name
            drivers.remove(d)
            return toret
    return None


def search_driver_id(driver_name, drivers):
    for d in drivers:
        if d.name == driver_name:
            return d.id
    return None


class TeamHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            username = user.nickname()
            is_admin = users.is_current_user_admin()
            access_link = users.create_logout_url("/teams")
        else:
            username = "login"
            access_link = users.create_login_url("/teams")
            is_admin = False

        drivers = Driver.query().fetch()
        teams_raw = Team.query().order(Team.name).fetch()

        teams = list(dict())

        for t in teams_raw:
            driver1 = t.driver1
            driver2 = t.driver2
            current_team = dict()
            current_team["name"] = t.name
            if driver1:
                name = search_driver_name(driver1, drivers)
                if name:
                    current_team["driver1"] = name
            if driver2:
                name = search_driver_name(driver2, drivers)
                if name:
                    current_team["driver2"] = name
            teams.append(current_team)

        susts = {
            "teams": teams,
            "freelance": drivers,
            "username": username,
            "is_admin": is_admin,
            "access_link": access_link
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("teams.html", **susts))

    def post(self):
        post_type = self.request.get('form', 'ERROR')
        nombre_old = self.request.get('old-name', 'ERROR')
        nombre = self.request.get('name', 'ERROR')
        piloto1 = self.request.get('driver1', 'ERROR')
        piloto2 = self.request.get('driver2', 'ERROR')

        if post_type == "insert" and nombre:
            team = Team.query(Team.name == nombre_old).fetch()[0]
            if not team:
                team = Team()
                team.name = nombre
                if piloto1 != "" or piloto2 != "":
                    drivers = Driver.query().fetch()
                    if piloto1 != "":
                        id1 = search_driver_id(piloto1, drivers)
                        if id1:
                            team.driver1 = id1
                    if piloto2 != "":
                        id2 = search_driver_id(piloto2, drivers)
                        if id2:
                            team.driver2 = id2
                team.put()

        elif post_type == "modify" and nombre:
            team = Team.query(Team.name == nombre_old).fetch()[0]
            team.name = nombre
            drivers = Driver.query().fetch()
            if piloto1 != 'ERROR':
                team.driver1 = int(search_driver_id(piloto1, drivers))
            if piloto2 != 'ERROR':
                team.driver2 = int(search_driver_id(piloto2, drivers))
            team.put()

        elif post_type == "remove" and nombre:
            team = Team.query(Team.name == nombre).fetch(1)[0]
            team.key.delete()

        elif post_type == "freelance" and nombre:
            teamlist = Team.query(Team.name == nombre).fetch(1)
            length = len(teamlist)
            team = teamlist[length - 1]
            if piloto1 == 'ERROR':
                team.driver2 = None
            elif piloto2 == 'ERROR':
                team.driver1 = None
            team.put()

        else:
            pass


app = webapp2.WSGIApplication([
    ('/teams', TeamHandler)
], debug=True)
