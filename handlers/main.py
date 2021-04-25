#!/usr/bin/env python

"""
Se muestra la clasificacion de pilotos y se podran insertar pilotos nuevos. Tambien es posible modificar y eliminar
pilotos ya existentes. Todos estos datos son guardados en data.json
"""

import webapp2
from webapp2_extras import jinja2
import json


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # read file
        with open('data.json', 'r') as f:
            data = json.load(f)
        drivers = list(data["drivers"])

        susts = {
            "drivers": drivers
        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("main.html", **susts))

    def post(self):
        post_type = self.request.get('form', 'ERROR')
        if post_type == "insert":
            nombre = self.request.get('name', 'ERROR')
            id_piloto = self.request.get('id', 'ERROR')
            puntos = self.request.get('score', 'ERROR')
            with open('data.json', 'a') as f:
                data = json.load(f)
                data["drivers"].append({"id": id_piloto, "name": nombre, "score": puntos})
        elif post_type == "modify":
            id_piloto = self.request.get('id', 'ERROR')
            puntos = self.request.get('score', 'ERROR')
            with open('data.json', 'r') as f:
                data = json.load(f)
                for d in data:
                    if d["id"] == id_piloto:
                        driver = d
                        break
            driver["score"] = puntos
            with open('data.json', 'w') as f:
                json.dump(driver, f)
        else:
            pass


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
