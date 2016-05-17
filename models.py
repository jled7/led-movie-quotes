# CTRL + SHIFT + O to import  
from google.appengine.ext import ndb


class MovieQuote(ndb.Model):
    ''' Model object used to store MovieQuotes in the datastore.'''
    quote = ndb.StringProperty()
    movie = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now_add=True)