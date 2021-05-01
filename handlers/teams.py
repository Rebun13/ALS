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


class TeamHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            is_admin = users.is_current_user_admin()
        else:
            user_name = None
            is_admin = False

        drivers = Driver.query().fetch()
        teams_raw = Team.query().fetch()

        teams = list(dict())

        for t in teams_raw:
            driver1 = t.driver1
            driver2 = t.driver2
            current_team = dict()
            current_team["name"] = t.name
            if driver1:
                name = search_driver_name(driver1.id, drivers)
                if name:
                    current_team["driver1"] = name
            if driver2:
                name = search_driver_name(driver2.id, drivers)
                if name:
                    current_team["driver2"] = name
            teams.append(current_team)

        susts = {
            "teams": teams,
            "freelance": drivers
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("teams.html", **susts))

    def post(self):
        post_type = self.request.get('form', 'ERROR')
        nombre = self.request.get('name', 'ERROR')
        piloto1 = self.request.get('driver1', 'ERROR')
        piloto2 = self.request.get('driver2', 'ERROR')

        if post_type == "insert" and nombre:
            # Store the new driver
            team = Team(name=nombre)
            team.put()

        elif post_type == "modify" and nombre:
            team = Team.query(Team.name == nombre).fetch()[0]
            team.name = nombre
            if piloto1:
                team.driver1 = int(piloto1)
            if piloto2:
                team.driver2 = int(piloto2)
            team.put()

        elif post_type == "remove" and nombre:
            team = Team.query(Team.name == nombre).fetch()[0]
            team.delete()

        else:
            pass


app = webapp2.WSGIApplication([
    ('/teams', TeamHandler)
], debug=True)
