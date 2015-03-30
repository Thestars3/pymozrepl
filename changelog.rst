변경사항
==============

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
