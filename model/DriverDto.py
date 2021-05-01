#!/usr/bin/env python


from google.appengine.ext import ndb


class Driver(ndb.Model):
    id = ndb.IntegerProperty(required=True, indexed=True)
    name = ndb.StringProperty(required=True)
    score = ndb.IntegerProperty(required=True)
