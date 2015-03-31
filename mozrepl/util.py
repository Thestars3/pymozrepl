#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import cookielib
import json
#from ufp.terminal.debug import print_ as debug

def convertToJs(arg):
	"""
	입력받은 값을 javascript에서 사용 가능한 값으로 변환합니다.
	
	:param arg: 변환할 값. 만약 list와 tuple타입을 인자로 준다면, 포함된 값은 :py:func:`~mozrepl.util.convertToJs` 함수가 변환 할 수 있는 값이어야 합니다.
	:type arg: int, float, None, unicode, bytes, bool, str, dict, tuple, list, :py:class:`~mozrepl.type.Object`, :py:class:`~mozrepl.type.Function`, :py:class:`~mozrepl.type.Array`, :py:class:`~mozrepl.type.Raw`
	:return: javascript에서 사용 할 수 있는 값.
	:rtype: unicode
	"""
	if arg is None:
		return 'null'
	
	if isinstance(arg, (int, float)):
		return unicode(arg)
	
	if isinstance(arg, unicode):
		return repr(arg.encode('UTF-8'))
	
	if isinstance(arg, str):
		return repr(arg)
	
	if isinstance(arg, bool):
		return 'true' if arg else 'false'
	
	if isinstance(arg, dict):
		buffer = lambda (k, v): '{k}: {v}'.format(k=convertToJs(k), v=convertToJs(v))
		buffer = map(buffer, arg.items())
		buffer = ', '.join(buffer)
		return '{{{0}}}'.format(buffer)
	
	if isinstance(arg, (tuple, list)):
		buffer = map(convertToJs, arg)
		buffer = ', '.join(buffer)
		return '[{0}]'.format(buffer)
	
	from .type import Object
	if isinstance(arg, Object):
		return unicode(arg)
	
	from .type import Raw
	if isinstance(arg, Raw):
		return unicode(arg)
	
	raise TypeError('"{type}" 타입은 변환 할 수 없는 타입입니다.'.format(type=type(arg)))

def getCookiesFromHost(repl, host):
	"""
	host와 일치하는 쿠키를 cookielib.Cookie형식으로 가져옵니다.
	
	:param repl: mozrepl.Mozrepl 객체
	:type repl: :py:class:`~mozrepl.Mozrepl`
	:param host: 호스트
	:type host: unicode
	:yield: 각 cookielib.Cookie.
	"""
	from .type import Object
	iter = Object.makeNotinited(repl)
	repl._rawExecute('{iter} = Services.cookies.getCookiesFromHost({host})'.format(iter=iter, host=convertToJs(host)))
	while repl.execute('{iter}.hasMoreElements()'.format(iter=iter)):
		buffer = repl.execute("""
		let buffer = {iter}.getNext().QueryInterface(Ci.nsICookie);
		JSON.stringify(buffer);
		""".format(iter=iter))
		cookie = json.loads(buffer)
		
		domain = cookie.get('host', None)
		initial_dot = domain.startswith(".")
		
		expires = cookie.get('expires', None)
		if expires == 0:
			expires = None
		
		yield cookielib.Cookie(
			0,
			cookie.get('name', None),
			cookie.get('value', None),
			None,
			False,
			domain,
			cookie.get('isDomain', None),
			initial_dot,
			cookie.get('path', None), 
			False, 
			cookie.get('isSecure', None), 
			expires,
			cookie.get('isSession', None),
			None, 
			None,
			{}
			)
	pass
