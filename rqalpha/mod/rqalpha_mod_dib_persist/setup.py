#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import (
    find_packages,
    setup,
)

setup(
    name='rqalpha_mod_dib_persist',
    version='0.0.1',
    description='rqalpha-mod-dib-persist',
    packages=find_packages(exclude=[]),
    author='liuzeyu',
    author_email='liuzeyu@dibgroup.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    zip_safe=False,
)
