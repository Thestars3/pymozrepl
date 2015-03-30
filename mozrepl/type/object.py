#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
#from ufp.terminal.debug import print_ as debug

from ..exception import Exception as MozException
from ..util import convertToJs

class Object(object):
	"""
	만약, 이 객체에 존재하는 속성의 이름과 같은 자바스크립트 오브젝트의 속성에 접근하려면, 사전 형식(__getitem__, __setitem__, __delitem__)으로 원소에 접근하십시오. 그 외에는 모두 속성을 호출하듯이 접근할 수 있습니다.
	
	__eq__, __contains__, __iter__ 메소드가 구현되어 있습니다.
	
	Iterator는 내부적으로, 자바스크립트의 Iterator 오브젝트를 사용합니다. 만약 해당 오브젝트에 Iterator가 구현되지 않았다면, 반환 결과는 Iterator의 구현을 따릅니다.
	
	.. caution:: 클로져가 구현되지 않았습니다. context에 의존적인 object의 속성을 참조 할때, Function타입은 실행하지 마십시오.
	
	..
	   자바 스크립트의 오브젝트는 파이썬의 사전과 유사하다.
	   자바 스크립트의 오브젝트의 각 요소는 모두 개별 요소로 존재한다.
	   만약, Mozrepl.execute 메소드를 통해 오브젝트를 반환받은 경우, 이 오브젝트는 참조값으로 존재하는가? 아니면, 복제되는가?
	   참조값으로 생각한다면, 이 값에 접근 할때 마다 접속후 연산할 필요성이 있다. 그러나, 이렇게 하면, 속도가 지연된다.
	   JSON으로 덤프해오게 된다면, 속성 값이 변경될 경우를 처리하지 못한다. 참조값으로 처리하기로 한다.
	   TODO : 편의를 위해 속성값을 포함하여 오브젝트 내용을 복사해오는 클래스를 따로 작성한다.
	"""
	def __init__(self, repl, uuid):
		self.__dict__['_repl'] = repl
		self.__dict__['_uuid'] = uuid
	
	@property
	def reference(self):
		"""
		자바스크립트에서 이 오브젝트에 대한 참조값.
		
		만약, 자바스크립트에서 직접 이 오브젝트에 대해 접근하기를 원한다면, 이 속성을 통해 변수 이름을 얻을 수 있습니다. 예컨데, 다음과 같이 사용 할 수 있습니다.
		
		.. code-block:: python
		
			>>> import mozrepl
			>>> repl = mozrepl.Mozrepl()
			>>> obj = repl.execute('repl')
			>>> obj.reference
			u'__pymozrepl_c8d7323280c54d09809e2dd7d34d1c70.ref["1e1c7ae3-c1fc-4664-b57f-1281bdc1c996"]'
			>>> repl.execute('var value = ' + obj.reference)
		"""
		return '{baseVar}.ref["{uuid}"]'.format(baseVar=self._repl._baseVarname, uuid=self._uuid)
	
	def __eq__(self, other):
		return self._repl.execute('{other} == {reference}'.format(other=convertToJs(other), reference=self.reference))
	
	def __contains__(self, item):
		return self._repl.execute('{item} in {reference}'.format(item=convertToJs(item), reference=self.reference))
	
	def __getattr__(self, name):
		return self[name]
	
	def __setattr__(self, name, value):
		self[name] = value
	
	def __delattr__(self, name):
		del self[name]
	
	def __iter__(self):
		self._repl._rawExecute('{baseVar}.buffer = Iterator({reference}, true)'.format(baseVar=self._repl._baseVarname, reference=self.reference))
		while True:
			try:
				value = self._repl.execute('{baseVar}.buffer.next()'.format(baseVar=self._repl._baseVarname))
				yield tuple(value) if isinstance(value, Array) else value
			except MozException, e:
				if e.typeName == 'StopIteration':
					raise StopIteration
				raise e
		pass
	
	def __repr__(self):
		return self._repl._rawExecute(self.reference)
	
	def __getitem__(self, key):
		return self._repl.execute('{reference}[{key}]'.format(reference=self.reference, key=convertToJs(key)))
	
	def __setitem__(self, key, value):
		self._repl._rawExecute('{reference}[{key}] = {value}'.format(reference=self.reference, key=convertToJs(key), value=value))
	
	def __delitem__(self, key):
		self._repl._rawExecute('delete {reference}[{key}]'.format(reference=self.reference, key=convertToJs(key)))
	
	def __del__(self):
		self._repl._rawExecute('delete {reference}'.format(reference=self.reference))
	

from .array import Array
