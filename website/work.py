#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

import core
import models
import util

import time
import logging

from google.appengine.ext import db

if __name__ == '__main__':
    logging.info('begin cron tasks.')
    newUsers = db.GqlQuery("SELECT * "
                           "FROM User "
                           "ORDER BY date ASC")
    succeed = 0
    for user in newUsers:
        grades = core.jwc.Grades(user.student_no, user.passwd)
        content = grades.getGrades()
        if content:
            succeed += 1
            util.SendMail(user.email, user.student_no, content)

            student_no = user.student_no
            passwd = user.passwd    # backup
            email = user.email
            db.delete(user) # delete from list.

            user_done = models.User_done(key_name=student_no)   # add to done_list.
            user_done.student_no = student_no
            user_done.passwd = passwd
            user_done.email = email
            user_done.done_date = util.time_now()   # +8.
            user_done.put()  # store

        else:
            if succeed == 0:
                break
            else:
                time.sleep(1)

    logging.info('%d user succeed.', succeed)