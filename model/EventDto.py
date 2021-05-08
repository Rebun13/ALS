#!/usr/bin/env python


from google.appengine.ext import ndb


class Event(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    country = ndb.StringProperty(required=True)
    date = ndb.DateProperty(required=True)
    image = ndb.BlobProperty()
