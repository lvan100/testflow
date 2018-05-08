#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

from TestFlow import Actuator

# 这么写可以防止IDEA格式化去掉没有使用的模块
__import__('TestDemo', fromlist=['*'])

process = {
    'users': {
        'driver_1': {
            'role': 'TestDemo.Driver'
        },
        'driver_2': {
            'role': 'TestDemo.Driver'
        }
    },
    'tasks': [
        {
            'user': 'driver_1',
            'action': {
                'name': 'login',
                'param': {
                    'phone': '11100010138'
                },
                'extract': {
                    "$.ticket": "ticket",
                    "$.phone": "phone"
                }
            }
        },
        {
            'user': 'driver_2',
            'action': {
                'name': 'login',
                'param': {
                    'phone': '11100010137'
                },
                'extract': {
                    "$.ticket": "ticket",
                    "$.phone": "phone"
                }
            }
        }
    ]
}

result = Actuator.invoke(process)
print(json.dumps(result, indent=1))
