#!/usr/bin/env python

"""
Se muestra la clasificacion de pilotos y se podran insertar pilotos nuevos. Tambien es posible modificar y eliminar
pilotos ya existentes. Todos estos datos son guardados en data.json
"""

import webapp2
from webapp2_extras import jinja2


class MainHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("main.html"))

    def post(self):
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("main.html"))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
