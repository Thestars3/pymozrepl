소개
===============

**pymozrepl는 Firefox MozREPL Add-on에 접근하기 위한 Python Interface를 제공합니다.**

.. image:: https://pypip.in/version/mozrepl/badge.png?text=version
    :target: https://pypi.python.org/pypi/mozrepl/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/mozrepl/badge.png
    :target: https://pypi.python.org/pypi/mozrepl/
    :alt: Supported Python versions
    
.. image:: https://pypip.in/status/mozrepl/badge.png
    :target: https://pypi.python.org/pypi/mozrepl/
    :alt: Development Status
    
.. image:: https://pypip.in/license/mozrepl/badge.png
    :target: https://pypi.python.org/pypi/mozrepl/
    :alt: License

특징
-------------------

* firefox mozrepl에 연결하기 위한 과정을 단축 할 수 있습니다.
* firefox mozrepl에 값을 전달하고 반환받은 결과에서 불필요한 텍스트를 자동으로 제거해줍니다.
* firefox mozrepl에 값을 전달하고 반환받은 결과를 Python의 기본 타입에 맞게 변환해줍니다.
* javascript object에 접근 하기 위한 인터페이스를 제공해줍니다.
* 기타 등등...

사용 예
-------------------

먼저, mozrepl Firefox Add-on을 `addons.mozilla.org <https://addons.mozilla.org/en-US/firefox/addon/mozrepl/>`_ 로 부터 설치한뒤, 서버를 시작합니다.

.. code-block:: python

	>>> import mozrepl
	>>> repl = mozrepl.Mozrepl()
	>>> repl.execute('window')
	[object ChromeWindow] - {0: {...}, 1: {...}, 2: {...}, 3: {...}, 4: {...}, close: function() {...}, stop: function() {...}, ...}
	>>> list(repl.execute(u'["a", 1, 2, 3, 4]'))
	[u'a', 1, 2, 3, 4]
	>>> repl.execute('content').document.title
	u'pymozrepl \\u2014 mozrepl 0.1a8 documentation'
	>>> import mozrepl.util
	>>> for cookie in mozrepl.util.getCookiesFromHost(repl, '.cpan.org'):
	... 	break
	...
	>>> cookie
	Cookie(version=0, name=u'css', value ...

도움말
-------------------

다음 문서를 참조 하십시오: http://pymozrepl.readthedocs.org/index.html.

수정사항
-------------------

`changelog.rst <https://github.com/Thestars3/pymozrepl/blob/master/changelog.rst>`_ 문서를 참조하세요.

라이센스
-------------------

`GPL v3 <https://github.com/Thestars3/pymozrepl/blob/master/COPYING>`_

개발자
-------------------

별님 <w7dn1ng75r@gmail.com>

파이썬 환경
-------------------

오직 2.7 버전대에서만 사용 할 수 있습니다.

설치 방법
-------------------

`설치 <http://pymozrepl.readthedocs.org/installation.html>`_ 문서를 참조하십시오.

소스 코드
-------------------

소스 코드는 다음 사이트에 올려져 있습니다: https://github.com/Thestars3/pymozrepl.
