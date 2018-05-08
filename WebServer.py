#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from functools import wraps

from flask import Flask, request, make_response

from Config import import_list
from TestFlow import Actuator, MetaData

for module in import_list:
    __import__(module, fromlist=['*'])

app = Flask(__name__)


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        result = fun(*args, **kwargs)
        resp = make_response(json.dumps(result))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent,Content-Type"
        resp.headers['Access-Control-Allow-Headers'] = allow_headers
        return resp

    return wrapper_fun


@app.route("/metadata")
@allow_cross_domain
def metadata0():
    return MetaData.metaData()


@app.route("/metadata/roles")
@allow_cross_domain
def roles():
    return MetaData.roleList()


@app.route("/metadata/actions")
@allow_cross_domain
def actions():
    role = request.args.get('role')
    return MetaData.actionList(role)


@app.route("/metadata/action")
@allow_cross_domain
def action0():
    role = request.args.get('role')
    action = request.args.get('action')
    return MetaData.actionInfo(role, action)


@app.route("/process/start", methods=['POST', 'OPTIONS'])
@allow_cross_domain
def invoke():
    if request.method == 'POST':
        return Actuator.invoke(request.json)
    return None


app.run('0.0.0.0')
