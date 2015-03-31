#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import re
import os.path
import sys

if sys.version_info >= (3,):
	raise RuntimeError('this module not supporting Python 3 yet.')

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = ''
with open('mozrepl/__init__.py', 'r') as fd:
	reg = re.compile(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]')
	for line in fd:
		m = reg.match(line)
		if m:
			version = m.group(1)
			break
		pass
	pass

if not version:
	raise RuntimeError('Cannot find version information')

setup(
	name             = 'mozrepl',
	version          = version,
	author           = '별님',
	author_email     = 'w7dn1ng75r@gmail.com',
	url              = 'http://thestars3.tistory.com/',
	description      = 'Firefox MozREPL Add-on에 접근하기 위한 인터페이스를 제공합니다.',
	packages         = [
			'mozrepl',
			'mozrepl.type'
		],
    package_dir      = {'mozrepl': 'mozrepl'},
    package_data     = {
		'': [
			'README.rst',
			'AUTHORS',
			'COPYING'
			]
		},
	zip_safe         = False,
	license          = "GPL v3",
	keywords         = ['mozrepl', 'firefox'],
	long_description = read('README.rst'),
	classifiers      = [
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 2 :: Only",
		"Environment :: Web Environment :: Mozilla",
		"Development Status :: 5 - Production/Stable",
		"Topic :: Utilities",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Operating System :: OS Independent",
		"License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
		],
	download_url     = "https://github.com/Thestars3/pymozrepl/releases",
	platforms        = ['OS Independent'],
	include_package_data = True
	)
