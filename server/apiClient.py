#!/usr/bin/env python

import urllib,urllib2
from django.utils import simplejson as json


def create(data,table="json"):
    if table=="json":
        url="http://localhost:8080/api/create/json"
        #print json.dumps(data)
        #uData = urllib.urlencode(json.dumps(data))
        req = urllib2.Request(url, json.dumps(data))
        response = urllib2.urlopen(req)
        return response.read()
    else: print "wrong table : "+table

def delete(key,table="json"):
    if table=="json":
        url="http://localhost:8080/api/delete/json/"+key
        req = urllib2.Request(url,'')
        response = urllib2.urlopen(req)
        return response.read()
    else: print "wrong table : "+table
    
def get(key,table="json"):
    if table=="json":
        url="http://localhost:8080/api/get/json/"+key
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    else: print "wrong table : "+table

def update(key,newData,table="json"):
    if table=="json":
        url="http://localhost:8080/api/update/json/"+key
        req = urllib2.Request(url, json.dumps(newData))
        response = urllib2.urlopen(req)
        return response.read()
    else: print "wrong table : "+table
    
def list(size,table="json"):
    if table=="json":
        url="http://localhost:8080/api/list/json/"+str(size)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return json.loads(response.read())
    else: print "wrong table : "+table

d={"asd":12,"aedg":1}    
k= create(d)
print get(k)
u={"asgd":12,"safdg":"sd","aedg":1}
update(k,u)
print get(k)
print "list"

print list(5)
print delete(k)
