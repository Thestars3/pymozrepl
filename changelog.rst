변경사항
==============

v0.1a5
------

+ mozrepl.type.Function에서 발생하던 'TypeError: must be type, not Function' 오류를 수정. [`tb69wn6127`_]
+ mozrepl.Mozrepl.for_ 메소드를 제거. [`tb69wn6127`_]
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
