변경사항
==============

v1.0.6
-------

+ 오류가 발생했을때, 정상적으로 전달받지 못하던 버그 수정. [`tb69wn6127`_]
+ mozrepl.util.getCookiesFromHost 함수가 정상적으로 작동하지 않던 버그 수정. [`tb69wn6127`_]

v1.0.5
-------

+ mozrepl.Exception 클래스에 __getitem__, __contains__ 메소드 추가. [`tb69wn6127`_]

v1.0.4
-------

+ mozrepl.Mozrepl.execute 메소드를 사용할때, 반환받는 값에 현재 프롬프트('repl\\d*>')가 포함되면 비정상적으로 작동하 던 점 수정. [`tb69wn6127`_]
+ mozrepl.Mozrepl.execute 메소드의 반환 받는 값에서 -inf 등의 타입과 long 등을 지원 하도록 개선. [`tb69wn6127`_]
+ 오류 처리를 향상. [`tb69wn6127`_]
	+ mozrepl.Exception 클래스에서 javascript 오류 객체의 속성 정보를 확인 할 수 있게 함. [`tb69wn6127`_]
	+ 일부 오류의 경우 오류 이름을 가져오지 못한 던 점 수정. [`tb69wn6127`_]
+ mozrepl.Mozrepl.connect 메소드 사용시, 기존 문맥을 소실하던 버그 수정. [`tb69wn6127`_]

v1.0.3
-------

+ mozrepl.util.convertToJs 함수가 json 규격을 준수하도록 수정. [`tb69wn6127`_]

v1.0.2
-------

+ mozrepl.util.convertToJs 함수에서 long 타입을 처리 할 수 있도록 개선. [`tb69wn6127`_]

v1.0.1
-------

+ mozrepl.util.convertToJs 함수에서 bool 타입을 처리 할 수 있도록 개선. [`tb69wn6127`_]

v1.0.0
-------

+ 정식 버전 릴리즈. [`tb69wn6127`_]
+ mozrepl.util.getCookiesFromHost 메소드의 수행 속도를 향상. [`tb69wn6127`_]

v0.1b7
-------

+ Object 클래스에 makeNotinited 클래스 메소드 추가. [`tb69wn6127`_]

v0.1b6
-------

+ Mozrepl.execute 메소드 사용시 발생하던, 'UnicodeEncodeError: 'ascii' codec can't encode character' 오류 수정. [`tb69wn6127`_]

v0.1b5
-------

+ mozrepl.util.convertToJs 함수에서 dict 타입도 처리 할 수 있게 함. [`tb69wn6127`_]
+ mozrepl.type.Raw로 mozrepl.util.convertToJs 함수에서 원본 코드가 그대로 전달될 수 있도록 함. [`tb69wn6127`_]

v0.1b4
-------

+ object 타입에서 reference 속성이 제거되고, 그 기능을 Object.__unicode__ 메소드가 담당하게됨. [`tb69wn6127`_]

v0.1b3
-------

+ util.getCookiesFromHost 속도를 향상. [`tb69wn6127`_]

v0.1b2
-------

+ tuple과 list를 javascript 문장으로 변환하는 기능을 추가함. [`tb69wn6127`_]
+ type.Function.__call__ 메소드에서 kwargs 인자를 제거. [`tb69wn6127`_]
+ util.getCookiesFromHost 함수가 정상 작동 되도록 업데이트. [`tb69wn6127`_]
+ Mozrepl.execute에서 'IOError: [Errno 24] Too many open files' 오류가 발생하던 버그 수정. [`tb69wn6127`_]

v0.1b1
-------

+ Object iterator가 정상적으로 작동하지 않는 문제 해결. [`tb69wn6127`_]

v0.1a14
-------

+ 함수 바인딩 기능을 execute명령에서 제거하고, Object의 속성에 존재하는 메소드에 대해서 바인딩되도록 수정. [`tb69wn6127`_]

v0.1a13
-------

+ 기존에 Mozrepl.execute 메소드에서 for이나 while과 같은 연산자가 처음에 오는 js코드를 넘기면 발생하던 무한 응답 지연 현상 수정. [`tb69wn6127`_]
+ Firefox MozREPL 1.1.2에서 발생하는 UNICODE 문자열 오류(ASCII 코드 범위를 넘어서는 문자열을 사용하면 발생하는 'socket.error: [Errno 32] Broken pipe' 오류 또는 무한 응답 대기 현상)를 회피 처리. [`tb69wn6127`_]

v0.1a12
-------

+ mozrepl.Mozrepl.execute 메소드에서 type 옵션을 제거함. [`tb69wn6127`_]
	+ nolastcmd 옵션의 기능을 자동 분석 프로세스가 담당하게 됨. [`tb69wn6127`_]
	+ noreturn 옵션의 기능을 _rawExecute 메소드가 담당하게 됨. [`tb69wn6127`_]
	+ repr 옵션의 기능을 _rawExecute 메소드가 담당하게 됨. [`tb69wn6127`_]

v0.1a11
-------

+ 설치 오류 수정. [`tb69wn6127`_]

v0.1a10
-------

+ type.Function에 __call__메소드 구현 마무리. [`tb69wn6127`_]

v0.1a9
-------

+ 리턴 받은 js object에 __del__ 메소드를 구현. [`tb69wn6127`_]
+ js array에 __len__ 메소드 구현. [`tb69wn6127`_]
+ js object에 __contains__, __eq__ 메소드 구현. [`tb69wn6127`_]

v0.1a8
------

+ array type을 추가. [`tb69wn6127`_]
+ util.convertToCmd 함수를 제거. [`tb69wn6127`_]

v0.1a7
------

+ mozrepl.type.Function에서 발생하던 'TypeError: context is undefined' 오류를 수정. [`tb69wn6127`_]

v0.1a6
------

+ mozrepl.Mozrepl에 __repr__ 메소드를 구현. [`tb69wn6127`_]
+ mozrepl.type.Object에서 발생하던 'ReferenceError: x is not defined' 오류 수정. [`tb69wn6127`_]
+ mozrepl.util.convertToJs 함수를 추가. [`tb69wn6127`_]
+ mozrepl.type.Function의 __call__ 메소드를 개선함. [`tb69wn6127`_]
	+ 함수 및 오브젝트를 전달 가능해짐. [`tb69wn6127`_]
	+ 문자열에 \'문자가 포함되어 있을 경우를 처리함. [`tb69wn6127`_]
	+ int, None, float, str, mozrepl.type.Object 등의 형식을 인자로 줄 수 있도록 수정. [`tb69wn6127`_]

v0.1a5
------

+ mozrepl.type.Function에서 발생하던 'TypeError: must be type, not Function' 오류를 수정. [`tb69wn6127`_]
+ mozrepl.Mozrepl.for\_ 메소드를 제거. [`tb69wn6127`_]
+ mozrepl.Mozrepl.execute 메소드에서 빈 Array와 같은 오브젝트도 정상적으로 처리하지 못하던 점 수정. [`tb69wn6127`_]
+ mozrepl.type.Object에서 숫자를 통해 원소에 접근하고자 할때, 응답을 하지 않던 문제 수정. [`tb69wn6127`_]

v0.1a4
------

+ Mozrepl.execute 메소드에서 float형을 처리할 수 있도록 개선. [`tb69wn6127`_]
+ Mozrepl.execute 메소드에서 string형 파싱시 발생하던 콰우팅 문제 수정. [`tb69wn6127`_]

v0.1a3
------

+ Mozrepl.execute 메소드에 type옵션을 추가함. [`tb69wn6127`_]
+ Mozrepl.execute 메소드에서 object타입을 처리하도록 수정. [`tb69wn6127`_]
+ Mozrepl.execute 메소드에서 function타입을 처리하도록 수정. [`tb69wn6127`_]

v0.1a2
------

+ Mozrepl.execute 메소드에서 mozrepl에서 string형태로 값을 반환받을 경우 \"문자가 포함된 경우, 해당 문자까지만 잘라내는 경우 수정. [`tb69wn6127`_]

v0.1a1
------

+ pymozrepl 개발 시작. [`tb69wn6127`_]

.. _tb69wn6127: https://github.com/tb69wn6127
