#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function
from ufp.terminal.debug import print_ as debug
import mozrepl

repl = mozrepl.Mozrepl(7070)
debug(repl.execute('repl'))
