#!/usr/bin/python
# -*- coding: UTF-8 -*-

from TestFlow.MetaData import *


@role("司机")
def _module():
    pass


@action(
    description='司机登录',
    param={
        "phone": {
            "tip": "用户手机号"
        }
    },
    extract={
        "$.ticket": "ticket",
        "$.phone": "phone"
    }
)
def login(phone):
    return {
        'role': 1,
        'phone': phone,
        'ticket': phone
    }
