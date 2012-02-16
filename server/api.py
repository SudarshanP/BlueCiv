#!/usr/bin/env python

import cgi
import logging
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from django.utils import simplejson as json
from google.appengine.api import memcache

class Article(db.Model):
    link = db.LinkProperty()
    paragraphs = db.TextProperty()
    
class JsonDB(db.Model):
    jsonData=db.TextProperty()
    
class ApiGet(webapp.RequestHandler):
    def get(self,table,keyStr):
        if table=="json":
            jsonEntry=JsonDB.get(db.Key(keyStr))
            if jsonEntry:
                self.response.out.write(jsonEntry.jsonData)
            else:
                self.response.out.write("key not found "+keyStr)
        else:
            self.response.out.write("no such table "+table)
          
class ApiList(webapp.RequestHandler):
    def get(self,table,size):
        size=int(size)
        if table=="json":
            q = JsonDB.all()
            last_cursor = memcache.get('JsonDB_cursor')
            if last_cursor:
                q.with_cursor(last_cursor)
            entityList = q.fetch(size)
            lst=[]
            for entity in entityList:
                lst.append(entity.jsonData)
            cursor = q.cursor()
            self.response.out.write(json.dumps({"list":lst}))
            memcache.set('JsonDB_cursor', cursor)
        else:
            self.response.out.write("no such table "+table)
        
class ApiCreate(webapp.RequestHandler):        
    def post(self,table):
        if table=="json":
            jsonStr=cgi.escape(self.request.body)
            jsonEntry=JsonDB()
            jsonEntry.jsonData=jsonStr
            jsonEntry.put()
            self.response.out.write(jsonEntry.key())    

class ApiUpdt(webapp.RequestHandler):        
    def post(self,table,keyStr):
        if table=="json":
            jsonEntry=JsonDB.get(db.Key(keyStr))
            if jsonEntry:
                jsonStr=cgi.escape(self.request.body)
                jsonEntry.jsonData=jsonStr
                jsonEntry.put()
                self.response.out.write("updated "+keyStr)
            else:
                self.response.out.write("key not found "+keyStr)
        else:
            self.response.out.write("no such table "+table)

class ApiDelete(webapp.RequestHandler):
    def post(self,table,keyStr):
        if table=="json":
            logging.info(keyStr)
            jsonEntry=JsonDB.get(db.Key(keyStr))
            if jsonEntry:
                jsonEntry.delete()
                self.response.out.write("deleted "+keyStr)
            else:
                self.response.out.write("key not found "+keyStr)
        
def main():
    application = webapp.WSGIApplication([(r'/api/get/(.*)/(.*)', ApiGet),
                                          (r'/api/list/(.*)/(.*)', ApiList),
                                          (r'/api/create/(.*)', ApiCreate),
                                          (r'/api/update/(.*)/(.*)', ApiUpdt),
                                          (r'/api/delete/(.*)/(.*)', ApiDelete) ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
