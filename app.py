#!/usr/bin/env python
# -*- coding:UTF-8 -*-

from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "hellow world"


if __name__ == '__main__':
    app.run()
