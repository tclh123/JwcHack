#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

import httphelper
import jwc

def test():
    http = httphelper.HttpHelper(isGAE=False)
    html = http.get('http://www.google.com/')
    return html

if __name__ == '__main__':
    """ run at local """
    grades = jwc.Grades('13101249', 'passwd', isGAE=False)
    print grades.getGrades()