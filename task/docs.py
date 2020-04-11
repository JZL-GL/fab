#!/usr/bin/env python
# -*- coding:UTF-8 -*-


from invoke import Collection, task

@task
def clean(c, target=None):
    print(c['sphinx'])

@task
def build(c, target=None):
    print(c['sphinx'])

ns = Collection(clean, build)
ns.configure({'sphinx': {'target': "docs/_build"}})
