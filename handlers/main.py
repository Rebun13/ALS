#!/usr/bin/env python

"""
Se muestra la clasificacion de pilotos y se podran insertar pilotos nuevos. Tambien es posible modificar y eliminar
pilotos ya existentes. Todos estos datos son guardados en data.json
"""
import time

import webapp2
from webapp2_extras import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

# import model.DriverDto
from model.DriverDto import Driver


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            username = user.nickname()
            is_admin = users.is_current_user_admin()
            access_link = users.create_logout_url("/")
        else:
            username = "login"
            access_link = users.create_login_url("/")
            is_admin = False

        drivers = Driver.query().order(-Driver.score)

        susts = {
            "drivers": drivers,
            "username": username,
            "is_admin": is_admin,
            "access_link":  access_link
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("main.html", **susts))

    def post(self):
        post_type = self.request.get('form', 'ERROR')
        nombre = self.request.get('name', 'ERROR')
        id_piloto = self.request.get('id', 'ERROR')
        puntos = self.request.get('score', 'ERROR')

        if post_type == "insert" and id_piloto:
            id_piloto = int(id_piloto)
            puntos = int(puntos)
            # Store the new driver
            driver = Driver(id=id_piloto, name=nombre, score=puntos)
            driver.put()

        elif post_type == "modify" and id_piloto:
            id_piloto = int(id_piloto)
            puntos = int(puntos)

            driver = Driver.query(Driver.id == id_piloto).fetch()[0]
            print(driver)
            driver.score = puntos
            driver.put()

        elif post_type == "remove" and id_piloto:
            id_piloto = int(id_piloto)
            driver = Driver.query(Driver.id == id_piloto).fetch()[0]
            driver.key.delete()

        else:
            pass

        time.sleep(.5)
        self.redirect("/")


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
