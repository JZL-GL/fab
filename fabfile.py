#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from fabric import Connection

# from fabric import task
#
# from fabric import SerialGroup as Group
#
web02 = Connection(host="10.0.0.13", user="root", connect_kwargs={'password': "123456"})
# # print web02
# # web02.run('hostname')
# # results = Group(web01, web02).run('hostname')
#
# web01 = '10.0.0.13'
# web02 = '10.0.0.200'
#
# # for host in (web01, web02):
# # result = Connection(host,user='root',connect_kwargs={'password': "123456"}).run('hostname')
#
# # 继承了Connection的用法 connect_kwargs={"key_filename": "/Users/jzl/.ssh/id_rsa"}
# results = Group(web01,web02,user="root", connect_kwargs={'password': "123456"}).run('hostname')


from invoke import task
from fabric import task

# config = Config(overrides={'run': {'pty': 'True', 'warn': 'False'}})

web01 = Connection(host="10.0.0.200", user="root", connect_kwargs={'password': "123456"})


@task
def upload_and_unpack(c):
    # c.cd("/User")
    # c.run('ls')
    c.run('hostname')
    web01.run('hostname -I')
    web01.run('echo $PATH;w')
    web01.run('echo $SHELL')

