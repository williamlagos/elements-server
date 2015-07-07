#!/usr/bin/python
#
# This file is part of Coronae project.
# 
# Copyright (C) 2009-2012 William Oliveira de Lagos <william.lagos1@gmail.com>
#
# Coronae is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Coronae is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Coronae.  If not, see <http://www.gnu.org/licenses/>.
#

#from django.contrib.auth.models import User
from datetime import datetime

import re,string,urllib2,sys,os,json
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.escape

objs = json.load(open('elements.json','r'))

def append_path(path=".."):
    sys.path.append(os.path.abspath(path))

class Coronae(tornado.web.RequestHandler):
    def get(self):
	e = {'Coronae':'Welcome to your first coronae node.'}
	self.write(self.to_json(e))
    def to_json(self,e):
	return tornado.escape.json_encode(e)
    def templates(self):
        return '../../templates/'
    def do_request(self,url,data=""):
        request = urllib2.Request(url=url,data=data)
        request_open = urllib2.urlopen(request)
        response = request_open.read()
        request_open.close()
        return response
    def current_user(self):
        name = self.get_current_user()
        user = User.objects.all().filter(username=name)
        return user[0]
    def get_login_url(self):
        return u"/login"
    def get_current_user(self):
        user = self.get_cookie('user')
        if user: name = re.split('[\s"]+',string.strip(user))[1]
        else: name = ""
        return name
    def get_object_bydate(self,strptime,token,miliseconds=True):
        form = ''
        if miliseconds: form += '.%f'
        now = datetime.strptime(strptime,'%Y-%m-%d %H:%M:%S'+form)
        objects,relations = objs['tokens'][token]
        return now,objects,relations
    def authenticate(self,username,password):
        exists = User.objects.filter(username=username)
        if exists:
            if exists[0].check_password(password): 
                return exists
        else: return None
    def authenticated(self):
        name = self.get_current_user()
        if not name: 
            self.render('templates/enter.html')
            return False
        else:
            return True
        
class Runtime():
    def __init__(self,handlers,social=None):
        urlhandlers = handlers
        if not social: self.application = tornado.web.Application(urlhandlers); return 
        apis = json.load(open(social,'r'))
        self.application = tornado.web.Application(urlhandlers,autoescape=None,cookie_secret=True,
        twitter_consumer_key=apis['twitter']['client_key'],twitter_consumer_secret=apis['twitter']['client_secret'],
        facebook_api_key=apis['facebook']['client_key'],facebook_secret=apis['facebook']['client_secret'])
    def run(self,port=None):
        try:
            http_server = tornado.httpserver.HTTPServer(self.application)
            if port: http_server.listen(int(port))
            else: http_server.listen(8888)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt: sys.exit(0)
