#!/usr/bin/env python

"""
Se muestra el calendario de carreras.
"""
import webapp2
import time
from datetime import datetime
import jinja2
from google.appengine.api import users
# from PIL import Image
from google.appengine.api import images

from model.EventDto import Event

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader('templates'),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class EventHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            username = user.nickname()
            is_admin = users.is_current_user_admin()
            access_link = users.create_logout_url("/event")
        else:
            username = "login"
            access_link = users.create_login_url("/event")
            is_admin = False
        print(username)
        events = Event.query().order(Event.date)
        susts = {
            "events": events,
            "username": username,
            "is_admin": is_admin,
            "access_link":  access_link
        }

        template = JINJA_ENVIRONMENT.get_template("event.html")
        self.response.write(template.render(susts))

    def post(self):
        name = self.request.get('event-name-input', 'ERROR')
        action = self.request.get('form', 'ERROR')
        country = self.request.get('event-country-input', 'ERROR')
        date_str = self.request.get('event-date-input', 'ERROR')
        image_file = self.request.get('event-image-input', None)

        if action == 'remove':
            event = Event.query(Event.name == name).fetch(1)[0]
            event.key.delete()

        elif name and country and date_str:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            event = Event(name=name, country=country, date=date)
            if image_file is not None:
                event.image = images.resize(image_file, 200, 200)
            event.put()
            time.sleep(1)

        self.redirect("/event")


app = webapp2.WSGIApplication([
    ('/event', EventHandler)
], debug=True)
