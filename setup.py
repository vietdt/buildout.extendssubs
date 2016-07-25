# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

version = "0.1"

tests_require=['zc.buildout', 'zope.testing', 'zc.recipe.egg']

setup(
    name="buildout.extendssubs",
    version=version,
    description="Enable buildout assignments substitution for extends option.",
    keywords='buildout extension extends assignment substitution',
    author='Viet Dinh',
    author_email='vietdt@gmail.com',
    url='https://github.com/vietdt/buildout.extendssubs',
    packages = find_packages('src'),
    package_dir = {'':'src'},
    namespace_packages=['buildout'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools',
                      'zc.buildout'
                      ],
    entry_points={'zc.buildout.extension': ['ext = buildout.extendssubs:ext']},
    )

