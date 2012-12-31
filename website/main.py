#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

import os
import urllib
import hashlib
import re

import core
import models
import util
#import httphelper
#import config

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
        student_no = self.request.get('uid')
        passwd = self.request.get('passwd')
        email = self.request.get('email')
        if len(student_no)<8 or len(passwd)<6 or len(email)<5:  # TODO 验证不符合要求的输入
            self.redirect('/')
            return

        # Grab!
        #grades = core.jwc.Grades(student_no, passwd)
        #content = grades.getGrades()

        ############ START      #TODO 本地没问题，传上GAE去有问题，http的cookie保存不住？？搞不出来，暂时不想搞了，头大

        http = core.httphelper.HttpHelper()

        html = http.get(core.config.getURL(student_no, 'Login'))        # 登陆页面

        m = re.search('var sharedValue = (-?\d+)', html)
        shared_value = m.group(1)

        m = hashlib.md5()
        m.update(passwd)
        first = m.hexdigest()
        m = hashlib.md5()
        m.update(first + shared_value)
        ret = m.hexdigest()

        passwd = ret

        logging.info(http.cj)

        logging.info('login post')
        http.post(core.config.getURL(student_no, 'UsersControl'),
            uid = student_no,
            password = passwd,
            command = 'studentLogin'
        )

        cj = http.cj #backup

        http = core.httphelper.HttpHelper()
        http.cj = cj

        logging.info(http.cj)

        logging.info('query get')
        html = http.get(core.config.getURL(student_no, 'query_person_score'))

#        http = core.httphelper.HttpHelper()
#        http.add_cookie('JSESSIONID', value, '125.76.215.232')
        logging.info(http.cj)

        c = re.compile(r'(.*?)<body>(.*?)</body>', re.S)
        m = c.match(html)
        body = m.group(2)
        body = body.replace('../../resources/images/', 'static/jwc/')
        content = body.decode('gbk')


        ############  END

        if not content:     # 如果此时网站不能正常访问，则加入列表，自动后台 cron job
            # add to list.
            user = models.User(key_name=student_no)    # uid is key.
            user.student_no = student_no
            user.passwd = passwd
            user.email = email
            user.date = util.time_now()   # +8.
            user.put()  # store
            template_values = {
                'user': user
            }
            template = jinja_environment.get_template('wait-for-email.html')
            self.response.out.write(template.render(template_values))
            return

        logging.info('%s done.' % student_no)

        user_done = models.User_done(key_name=student_no)   # add to done_list.
        user_done.student_no = student_no
        user_done.passwd = passwd
        user_done.email = email
        user_done.done_date = util.time_now()   # +8.
        user_done.put()  # store

        template_values = {
            'content': content
        }
        template = jinja_environment.get_template('showgrades.html')
        self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/submit', Submit)
    ],debug=True)