#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from invoke import task


@task
def hello(c):
    c.run("hostname")
    print("Hello World!")


@task
def greet(c, name):
    """
    A test for shell command.
    Second line.
    """
    c.run("echo {}加油!".format(name))
