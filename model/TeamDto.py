#!/usr/bin/env python


from google.appengine.ext import ndb


class Team(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    driver1 = ndb.IntegerProperty()
    driver2 = ndb.IntegerProperty()
