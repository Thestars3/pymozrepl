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
	
def openTab(repl, url, isPrivate=False, inNewWindow=False, inBackground=False, isPinned=False):
	"""
	Opens a new tab. The new tab will open in the active window or in a new window, depending on the inNewWindow option.
	
	:param repl: mozrepl 객체.
	:type repl: :py:class:`~mozrepl.Mozrepl`
	:param url: String URL to be opened in the new tab. This is a required property.
	:type url: unicode
	:param isPrivate: bool which will determine whether the new tab should be private or not. If your add-on does not support private browsing this will have no effect. See the private-browsing documentation for more information. Defaults to false.
	:type isPrivate: bool
	:param inNewWindow: If present and true, a new browser window will be opened and the URL will be opened in the first tab in that window. This is an optional property.
	:type inNewWindow: bool
	:param inBackground: If present and true, the new tab will be opened to the right of the active tab and will not be active. This is an optional property.
	:type inBackground: bool
	:param isPinned: If present and true, then the new tab will be pinned as an app tab.
	:type isPinned: bool
	"""
	buffer = """{baseVar}.modules.require('sdk/tabs').open({{ url: {url}, isPrivate: {isPrivate}, inNewWindow: {inNewWindow}, inBackground: {inBackground}, isPinned: {isPinned} }});""".format(
		baseVar = repl._baseVarname,
		url = convertToJs(url),
		isPrivate = convertToJs(isPrivate),
		inNewWindow = convertToJs(isPrivate),
		inBackground = convertToJs(inBackground),
		isPinned = convertToJs(isPinned)
		)
	tabs = repl.execute(buffer)

def getAllTabs(repl)	:
	"""
	접속한 브라우져에 존재하는 모든 탭 오브젝트를 가져옵니다.
	
	:param repl: mozrepl 객체.
	:type repl: :py:class:`~mozrepl.Mozrepl`
	:yield: 각 탭 :py:class:`~mozrepl.type.Object` 객체.
	"""
	buffer = """{baseVar}.modules.require('sdk/tabs');""".format(
		baseVar = repl._baseVarname
		)
	tabs = repl.execute(buffer)
	for tab in tabs:
		yield tab
	pass

def getCookiesFromHost(repl, host):
	"""
	Returns an generator of cookies that would be returned to a given host, ignoring the cookie flags isDomain, isSecure, and isHttpOnly. Therefore, if the specified host is "weather.yahoo.com", host or domain cookies for "weather.yahoo.com" and "yahoo.com" would both be returned, while a cookie for "my.weather.yahoo.com" would not.
	
	:param repl: mozrepl.Mozrepl 객체
	:type repl: :py:class:`~mozrepl.Mozrepl`
	:param host: The host unicode string to look for, such as "google.com". This should consist only of the host portion of the URI and should not contain a leading dot, port number, or other information.
	:type host: unicode
	:yield: An cookielib.Cookie objects representing the matching cookies.
	"""
	from .type import Object
	iter = Object.makeNotinited(repl)
	repl._rawExecute(
		"""
		{iter} = {baseVar}.modules.Services.cookies.getCookiesFromHost({host}); 
		null;
		""".format(
			iter=iter, 
			baseVar=repl._baseVarname,
			host=convertToJs(host)
		)
	)
	while repl.execute('{iter}.hasMoreElements()'.format(iter=iter)):
		buffer = repl.execute(
			"""
			let {{Ci}} = {baseVar}.modules.require("chrome");
			let buffer = {iter}.getNext().QueryInterface(Ci.nsICookie);
			JSON.stringify(buffer);
			""".format(
				iter = iter,
				baseVar = repl._baseVarname
			)
		)
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
