#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'tclh123'

import urllib
import urllib2
import logging
import cookielib
import re
from google.appengine.api import urlfetch

def _encode_params(**kw):
    """
    Encode parameters.
    """
    args = []
    for k, v in kw.iteritems():
        qv = v.encode('utf-8') if isinstance(v, unicode) else str(v)
        args.append('%s=%s' % (k, urllib.quote(qv)))
    return '&'.join(args)

class HttpHelper:
    """Http 封装类"""
    def __init__(self, header=None, isGAE=True):
        self.cj = cookielib.CookieJar()
        self.header = header
        self.status_code = None
        self._isGAE = isGAE
    def get(self, url, **kw):
        logging.debug('GET %s' % url)
        return self._http_call(url, urlfetch.GET, **kw)
    def post(self, url, **kw):
        logging.debug('POST %s' % url)
        return self._http_call(url, urlfetch.POST, **kw)
    def add_cookie(self, name, value, domain):
        ck = cookielib.Cookie(version=0, name=name, value=value, port=None, port_specified=False, domain=domain, domain_specified=False, domain_initial_dot=False, path='/', path_specified=True, secure=False, expires=None, discard=True, comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(ck)
    def get_cookie_value(self, name):
        for i in self.cj._cookies.itervalues():
            for j in i['/'].itervalues():
                if j.name == name:
                    return j.value
        return None
    def _http_call(self, url, method, **kw):
        params = _encode_params(**kw)   #params is a str
        if method == urlfetch.GET:
            http_url = '%s?%s' % (url, params) if params!='' else url
            http_body = None
        else:
            http_url = url
            http_body = params

        req = urllib2.Request(
            url=http_url,
            data=http_body,
            headers=self._getHeaders(self.cj)
        )

        # 如果不使用GAE
        if not self._isGAE:
            opener = urllib2.build_opener()
            resp = opener.open(req)
            html = resp.read()
            # Load the cookies from the response
            str_set_ck = resp.headers.get('set-cookie')
            if str_set_ck:
                m = re.match(r'(.*?)=(.*?);', str_set_ck)
                if m:
                    if m.group(2) != 'deleted':
                        self.add_cookie(m.group(1), m.group(2), '')
            return html

        # 使用GAE
        resp = urlfetch.fetch(url=http_url,
            payload=http_body,
            method=method,
            headers=self._getHeaders(self.cj),
            deadline=10
        )
        self.status_code = resp.status_code # 200.
        str_set_ck = resp.headers.get('set-cookie')
        if str_set_ck:
            m = re.match(r'(.*?)=(.*?);', str_set_ck)
            if m:
                if m.group(2) != 'deleted':
                    self.add_cookie(m.group(1), m.group(2), '')    #理论上不用了，开始是因为登陆后跨域了，cookie的domain不一样
        return resp.content
    def _getHeaders(self, cj):
        headers = {
            'Accept-Encoding' : 'utf-8',
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)'
            #'Cookie' : self._makeCookieHeader(cj)
        } if self.header is None else self.header
        headers['Cookie'] = self._makeCookieHeader(cj)
        return headers
    def _makeCookieHeader(self, cj):
        """
        cookielib.CookieJar to str_Cookie
        """
        cookieHeader = ""
        for i in cj._cookies.itervalues():
            for j in i['/'].itervalues():
                cookieHeader += '%s=%s;' % (j.name, j.value)
        return cookieHeader