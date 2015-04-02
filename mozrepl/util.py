#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
import cookielib
import json
#from ufp.terminal.debug import print_ as debug

class _JsonEncoder(json.JSONEncoder):
	def __init__(self, *args, **kwargs):
		super(_JsonEncoder, self).__init__(*args, **kwargs)
		
		from .type import Raw, Object
		self.types = {
			'Raw': Raw,
			'Object': Object
		}
	
	def default(self, obj):
		if isinstance(obj, self.types['Object']):
			return unicode(obj)
			
		if isinstance(obj, self.types['Raw']):
			return unicode(obj)
		
		return super(_JsonEncoder, self).default(obj)
	

def convertToJs(obj):
	"""
	입력받은 값을 javascript에서 사용 가능한 값으로 변환합니다.
	
	:param obj: 변환할 값. 만약 list와 tuple타입을 인자로 준다면, 포함된 값은 :py:func:`~mozrepl.util.convertToJs` 함수가 변환 할 수 있는 값이어야 합니다.
	:type obj: :py:class:`~mozrepl.type.Object`, :py:class:`~mozrepl.type.Function`, :py:class:`~mozrepl.type.Array`, :py:class:`~mozrepl.type.Raw` 외 python 기본 타입.
	:return: JSON string
	:rtype: unicode
	"""
	buffer = json.dumps(obj, cls=_JsonEncoder)
	return unicode(buffer)

def getAllTabs(repl)	:
	"""
	접속한 브라우져에 존재하는 모든 탭 오브젝트를 가져옵니다.
	
	:param repl: mozrepl 객체.
	:type repl: :py:class:`~mozrepl.Mozrepl`
	:yield: 각 탭 :py:class:`~mozrepl.type.Object` 겍체.
	"""
	buffer = """{baseVar}.modules.require('sdk/tabs');""".format(
		baseVar = repl._baseVarname
		)
	tabs = repl.execute(buffer)
	for i in range(tabs.length):
		yield tabs[i]
	pass

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
	repl._rawExecute('{iter} = Services.cookies.getCookiesFromHost({host}); null;'.format(iter=iter, host=convertToJs(host)))
	while repl.execute('{iter}.hasMoreElements()'.format(iter=iter)):
		buffer = """let buffer = {iter}.getNext().QueryInterface(Ci.nsICookie); JSON.stringify(buffer);""".format(
			iter = iter
			)
		buffer = repl.execute(buffer)
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
