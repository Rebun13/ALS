#!/usr/bin/env python

"""
Se muestra el calendario de carreras.
"""
import time
from datetime import datetime

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users

from model.EventDto import Event


class EventHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            user_name = user.nickname()
            is_admin = users.is_current_user_admin()
        else:
            user_name = None
            is_admin = False

        events = Event.query().order(Event.date)


        susts = {
            "events": events
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("event.html", **susts))

    def post(self):
        name = self.request.get('event-name-input', 'ERROR')
        action = self.request.get('form', 'ERROR')
        country = self.request.get('event-country-input', 'ERROR')
        date_str = self.request.get('event-date-input', 'ERROR')

        if action == 'remove':
            event = Event.query(Event.name == name).fetch(1)[0]
            event.key.delete()
            # TODO: redireccionar a la misma pagina

        elif name and country and date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            event = Event(name=name, country=country, date=date)
            event.put()
            time.sleep(1)

        self.redirect("/event")


app = webapp2.WSGIApplication([
    ('/event', EventHandler)
], debug=True)
