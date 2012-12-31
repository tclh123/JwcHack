#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

import os
import urllib

import core
import models
import util

import webapp2
import jinja2
import logging
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)+'/templates'))

class MainPage(webapp2.RequestHandler):
    def get(self):
        newUsers = db.GqlQuery("SELECT * "
                                "FROM User "
                                "ORDER BY date DESC LIMIT 10")
        doneUsers = db.GqlQuery("SELECT * "
                               "FROM User_done "
                               "ORDER BY done_date DESC LIMIT 10")

        template_values = {}
        if newUsers.count()!=0: template_values['newUsers'] = newUsers
        if doneUsers.count()!=0: template_values['doneUsers'] = doneUsers

#        for user in newUsers:
#            logging.info(user.student_no)
            # db.delete(user.key())

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Submit(webapp2.RequestHandler):
    def post(self):
        uid = self.request.get('uid')
        passwd = self.request.get('passwd')
        email = self.request.get('email')
        if len(uid)<8 or len(passwd)<6 or len(email)<5:  # TODO 验证不符合要求的输入
            self.redirect('/')

        try:
            user = models.User(key_name=uid)    # uid is key.
            user.student_no = uid
            user.passwd = passwd
            user.email = email
            user.date = util.time_now()   # +8.
            user.put()  # store
            self.redirect('/getgrades?' + urllib.urlencode({'student_no': uid}))
        except:
            self.redirect('/')

class GetGrades(webapp2.RequestHandler):
    def get(self):
        student_no = self.request.get('student_no')

        user_key = db.Key.from_path('User', student_no)
        user = db.get(user_key)
        grades = core.jwc.Grades(student_no, user.passwd)
        content = grades.getGrades()

        if not content:     # 如果此时网站不能正常访问，则加入列表，自动后台 cron job
            # add to list.
            template_values = {
                'user': user
            }
            template = jinja_environment.get_template('wait-for-email.html')
            self.response.out.write(template.render(template_values))
            return

        logging.info('%s done.' % student_no)

        passwd = user.passwd    # backup
        email = user.email
        db.delete(user_key) # delete from list.

        user_done = models.User_done(key_name=student_no)   # add to done_list.
        user_done.student_no = student_no
        user_done.passwd = passwd
        user_done.email = email
        user_done.done_date = util.time_now()   # +8.
        user_done.put()  # store

        template_values = {
            'content': grades.getGrades()
        }
        template = jinja_environment.get_template('showgrades.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/submit', Submit),
    ('/getgrades', GetGrades)
    ],debug=True)