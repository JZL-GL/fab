#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from invoke import task, Collection

import os


def _wrap_with(code):
    def out(text, bold=False):
        c = code

        if os.environ.get('FABRIC_DISABLE_COLORS'):
            return text

        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)

    return out


red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')

@task
def hello(c):
    print(red("Hello World!"))


@task
def greet(c, name):
    """
    A test for shell command.
    Second line.
    """
    c.run("echo {}加油!".format(name))
