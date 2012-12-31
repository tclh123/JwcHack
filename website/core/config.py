#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

IP_Campus_Network = '219.245.123.226'
IP_Telecom_Network = '125.76.215.232'

# /xdjwWebNew/systemAdmin/Login.jsp?command=studentLogin

URL_BASE = {
    'old' : '/xdjwWeb',     # 07 08 09
    'new' : '/xdjwWebNew'   # 10 11 (12?)
}
def getURL_BASE(student_no):
    grade = int(student_no[2:4])
    if grade-7<3: return URL_BASE['old']
    else: return URL_BASE['new']

URL_ACTION = {
    'Login' : '/systemAdmin/Login.jsp',
    'UsersControl' : '/Servlet/UsersControl',
    'query_person_score' : '/studentStatus/queryScore/query_person_score.jsp',
}

def getURL(student_no, action, network=''):
    ip = IP_Telecom_Network if network == 'Telecom' else IP_Campus_Network
    return 'http://' + ip + getURL_BASE(student_no) + URL_ACTION[action]