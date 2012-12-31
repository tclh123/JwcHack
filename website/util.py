#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

import logging
#import time
from google.appengine.api import mail
import datetime

def SendMail(to, student_no, content):
    """发邮件"""
    message = mail.EmailMessage(sender='tclh123@gmail.com',
        subject="%s's Grades from JwcHack" % student_no)
    message.to = to
    message.body = \
    """Hello %s:
        The following is your grades.
            %s
            //THE END.
            %s.""" % (student_no, content, str_time())
    message.send()
    logging.info('SendMail to %s, for %s.' % (to, student_no))

def time_now():
    return datetime.datetime.utcnow() + datetime.timedelta(hours=+8)

def str_time():
    """时间字符串"""
    return time_now().strftime('[%H:%M:%S]')
#    return time.strftime('[%H:%M:%S]')