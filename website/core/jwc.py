#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

import httphelper
import config
import re
import hashlib

class Grades:
    def __init__(self, student_no, passwd, isGAE=True):
        self._http = httphelper.HttpHelper(isGAE = isGAE)
        self.student_no = student_no
        self.passwd = passwd
        pass
    def getGrades(self):
        if not self._login():
            return None

        html = self._http.get(config.getURL(self.student_no, 'query_person_score'))
        if self._http.status_code != 200:
            return None

        c = re.compile(r'(.*?)<body>(.*?)</body>', re.S)
        m = c.match(html)
        body = m.group(2)
        body = body.replace('../../resources/images/', 'static/jwc/')
        return body.decode('gbk')
    def _login(self):
        html = self._http.get(config.getURL(self.student_no, 'Login'))
        if self._http.status_code != 200:
            return False

        m = re.search('var sharedValue = (-?\d+)', html)
        shared_value = m.group(1)
        passwd = self._hash_passwd(self.passwd, shared_value)
        self._http.post(config.getURL(self.student_no, 'UsersControl'),
            uid = self.student_no,
            password = passwd,
            command = 'studentLogin'
        )
        return True
    def _hash_passwd(self, passwd, shared_value):
        m = hashlib.md5()
        m.update(passwd)
        first = m.hexdigest()
        m = hashlib.md5()
        m.update(first + shared_value)
        return m.hexdigest()
