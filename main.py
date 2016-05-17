#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import os

from google.appengine.ext import ndb
import jinja2
import webapp2

from models import MovieQuote


# Jinja Environment instance necessary to use Jinja templates.
jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True)

# Strong Consistency
# Lock thing down until everything is done
# Generic key to serve as the parent
# When a Datastore entity is "put" into the Datastore really what happens is an event is created to do the "put" eventually,
# but flow is returned for speed reasons immediately (the real "put" is slow and done later on another thread). 
# Then the page was reloading before the "put" actually finished and new quotes weren't displayed.
# We added a parent key to all MovieQuote entities, then did an Ancesotr Query for entities that had that parent key.
# Ancestor Queries will look for unfinished events within the entity group and wait for them to complete before running the query.
# The potential problem with this solution is that If you had a million users you wouldn't want to lock down the entire Datastore using 
# a single shared parent for all users. If you were worried about scaling to milllions of people there needs to be a more clever mechanism in place
# where there are MANY entity groups using different parent keys if Strong Consistency is required.

PARENT_KEY = ndb.Key("Entity", "moviequote_root")

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("templates/moviequotes.html")
        '''self.response.write('Hello world!')'''
        #moviequotes_query = MovieQuote.query().order(-MovieQuote.last_touch_date_time) NOT STRONG CONSISTENCY
        moviequotes_query = MovieQuote.query(ancestor=PARENT_KEY).order(-MovieQuote.last_touch_date_time) # ASKING FOR THE ITEMS IN THE ROOT, WILL WAIT UNTIL ALL WORKS ARE DONE [STRONG CONSISTENCY]
        self.response.write(template.render({'moviequotes_query': moviequotes_query}))
        
class AddQuoteAction(webapp2.RequestHandler):
    def post(self):
        logging.info(str(self.request))
        quote = self.request.get('quote')
        movie = self.request.get('movie')
        # logging.info("Todo: Add Quote \"" + quote + "\" from movie \"" + movie + "\"")
        # self.response.write("Todo: Add Quote \"" + quote + "\" from movie \"" + movie + "\"")
        #new_moviequote = MovieQuote(parent = PARENT_KEY, quote=quote, movie=movie)
        new_moviequote = MovieQuote(parent = PARENT_KEY,
                                    quote=quote,
                                    movie=movie)
        new_moviequote.put()
        self.redirect(self.request.referer)
        
class InsertQuoteAction(webapp2.RequestHandler):
    def post(self):
        quote = self.request.get('quote')
        movie = self.request.get('movie')
        if self.request.get("entity_key"):
            # logging.info("URL Safe = \"" + self.request.get("entity_key") + "\"")
            moviequote_key = ndb.Key(urlsafe=self.request.get("entity_key"))
            # logging.info("String rep of REAL key = \"" + str(moviequote_key) + "\"")
            moviequote = moviequote_key.get()
            moviequote.quote = self.request.get("quote")
            moviequote.movie = self.request.get("movie")
            moviequote.put();
        else:
            new_moviequote = MovieQuote(parent = PARENT_KEY,
                                    quote=quote,
                                    movie=movie)
            new_moviequote.put()
        self.redirect(self.request.referer)

class DeleteQuoteAction(webapp2.RequestHandler):
    def post(self):
        moviequote_key = ndb.Key(urlsafe=self.request.get("entity_key"))
        moviequote_key.delete()
        self.redirect(self.request.referer)
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/addquote', AddQuoteAction),
    ('/insertquote', InsertQuoteAction),
    ('/deletequote', DeleteQuoteAction)
], debug=True)
