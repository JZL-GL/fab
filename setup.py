#!/usr/bin/env python
# -*- coding:UTF-8 -*-

setup(
    name='tester',
    version='0.1.0',
    packages=['tester'],
    install_requires=['invoke'],
    entry_points={
        'console_scripts': ['tester = tester.main:program.run']
    }
)
