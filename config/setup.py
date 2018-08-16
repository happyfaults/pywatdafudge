#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

setup(
    name='pywatdafudge_c',
    version='0.0.2a1',
    license='MIT License',
    description='The default config modules for pywatdafudge.',
    url='https://github.com/happyfaults/pywatdafudge',
    packages=find_packages('.'),
    package_dir={'': '.'},
    py_modules=[splitext(basename(path))[0] for path in glob('*.py')],
    include_package_data=True,
    zip_safe=False,
)