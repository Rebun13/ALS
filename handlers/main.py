#!/usr/bin/env python

"""
Se muestra la clasificacion de pilotos y se podran insertar pilotos nuevos. Tambien es posible modificar y eliminar
pilotos ya existentes. Todos estos datos son guardados en data.json
"""

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
            user_name = user.nickname()
            is_admin = users.is_current_user_admin()
        else:
            user_name = None
            is_admin = False

        drivers = Driver.query().order(-Driver.score)

        susts = {
            "drivers": drivers,
            "username": user_name,
            "is_admin": is_admin
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
            driver.score = puntos
            driver.put()

        elif post_type == "remove" and id_piloto:
            id_piloto = int(id_piloto)
            driver = Driver.query(Driver.id == id_piloto).fetch()[0]
            driver.delete()

        else:
            pass


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
