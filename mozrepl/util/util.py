#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import cookielib

__all__ = ['getCookiesFromHost']

def getCookiesFromHost(repl, host):
	"""
	:param repl: mozrepl.Mozrepl 객체
	:type repl: mozrepl.Mozrepl
	:param host: 호스트
	:type host: unicode
	:yield: 각 cookielib.Cookie.
	"""
	repl.console('let enum_ = Services.cookies.getCookiesFromHost("%(host)s");' % locals())
	while repl.console('enum_.hasMoreElements();'):
		repl.console('var cookie = enum_.getNext().QueryInterface(Ci.nsICookie);')
		
		#cookie['isHttpOnly'] = c('cookie.isHttpOnly')
		#cookie['expiry'] = c('cookie.expiry')
		
		name = repl.console('cookie.name')
		value = repl.console('cookie.value')
		domain = repl.console('cookie.host')
		path = repl.console('cookie.path')
		secure = repl.console('cookie.isSecure')
		discard = repl.console('cookie.isSession')
		domain_specified = repl.console('cookie.isDomain')
		
		expires = repl.console('cookie.expires')
		if expires == 0:
			expires = None
		
		initial_dot = domain.startswith(".")
		yield cookielib.Cookie(0, name, value, None, False, domain, domain_specified, initial_dot, path, False, secure, expires, discard, None, None, {})
	pass
	