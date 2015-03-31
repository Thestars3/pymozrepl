#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
from ufp.terminal.debug import print_ as debug

import mozrepl
repl = mozrepl.Mozrepl(7070)

iter = repl.execute('Services').cookies.getCookiesFromHost('www.naver.com')
debug(iter)
debug(iter.hasMoreElements())
debug(iter.getNext())
debug('='*72)
#debug( repr( repl.execute('this') ) )
#debug( repr( repl.execute('repl._workContext') ) )
#debug( type(type( repl.execute('repl') ) ))
#debug( repr( repl.execute('repl').home() ) )
#func = repl.execute('(function(){ return "mozrepl"; })') #__call__
#debug( repr( func() ) )

#for key, value in repl.execute('a = {"z": "10", "y": 20, 10:20};'):
	#debug(repr(key))
	#debug(repr(value))

import mozrepl.util
for cookie in mozrepl.util.getCookiesFromHost(repl, 'www.naver.com'):
	debug(repr(cookie))

#debug(repr(a))
#debug(list(a))
#debug(repr(a == 'a'))
