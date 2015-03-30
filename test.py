#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import mozrepl
repl = mozrepl.Mozrepl(7070)

a = repl.execute('repl.home')()

import mozrepl.util

for cookie in mozrepl.util.getCookiesFromHost(repl, '.cpan.com'):
	print(repr(cookie))
	
#print(repr(a))
#print(list(a))
#print(repr(a == 'a'))