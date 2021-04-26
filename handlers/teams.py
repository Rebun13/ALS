#!/usr/bin/env python

"""
Se muestra la informacion basica sobre los equipos, es decir, su nombre y sus pilotos. Ademas, se podran cambiar los
pilotos entre equipos. Todos estos datos son guardados en data.json
"""

import webapp2
from webapp2_extras import jinja2
import json


class TeamsHandler(webapp2.RequestHandler):
    def get(self):
        # read file
        with open('data.json', 'r') as f:
            data = json.load(f)
        drivers = list(data["drivers"])
        teams_raw = list(data["teams"])

        teams = dict()

        for t in teams:
            ids = t["drivers"]
            n = len(ids)
            d = []
            for i in range(n - 1):
                found_it = False
                j = 0
                m = len(drivers)
                while not found_it and j < m:
                    if drivers[j]["id"] == ids[i]:
                        found_it = True
                        d.append(drivers[j]["name"])
                        drivers.remove(j)
            teams[t["name"]] = d

        susts = {
            "teams": teams,
            "freelance": drivers
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("teams.html", **susts))


app = webapp2.WSGIApplication([
    ('/teams', TeamsHandler)
], debug=True)
