#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from fabric import Connection
from fabric import Config
from fabric import SerialGroup


# from fabric import SerialGroup as Group
# #  connect_kwargs={"key_filename": "/Users/jzl/.ssh/id_rsa"}
# results = Group(web01,web02,user="root", connect_kwargs={'password': "123456"}).run('hostname')
