#!/usr/bin/env python

"""
Se cargan los datos en la base de datos
"""
from datetime import datetime

import webapp2
from model.DriverDto import Driver
from model.TeamDto import Team
from model.EventDto import Event
import json


class LoaderHandler(webapp2.RequestHandler):
    def get(self):
        with open('data.json', 'r') as f:
            data = json.load(f)
        drivers = list(data["drivers"])
        teams = list(data["teams"])
        events = list(data["events"])

        for e in events:
            event = Event(name=e["name"], country=e["country"], date=datetime.strptime(e["date"], "%Y-%m-%d"))
            print(e["image"])
            if e["image"]:
                event.image = e["image"]
            event.put()

        for d in drivers:
            print(d)
            driver = Driver(id=d["id"], name=d["name"], score=d["score"])
            driver.put()

        for t in teams:
            team = Team(name=t["name"])
            dr = t["drivers"]
            if len(dr) > 0:
                team.driver1 = dr[0]
                if len(dr) > 1:
                    team.driver2 = dr[1]
            team.put()
        self.redirect("/")


app = webapp2.WSGIApplication([
    ('/load', LoaderHandler)
], debug=True)