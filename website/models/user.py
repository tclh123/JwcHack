#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

from google.appengine.ext import db

class User(db.Model):
    student_no = db.StringProperty()
    passwd = db.StringProperty()
    email = db.EmailProperty()
    date = db.DateTimeProperty(auto_now_add=True)

class User_done(db.Model):
    student_no = db.StringProperty()
    passwd = db.StringProperty()
    email = db.EmailProperty()
    done_date = db.DateTimeProperty(auto_now_add=True)