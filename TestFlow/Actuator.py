#!/usr/bin/python
# -*- coding: UTF-8 -*-

import copy
import sys
import threading

"""
线程本地变量:
  SERVER => 测试服务器地址
"""
localData = threading.local()


def invoke(process):
    """
    执行用户提交的动作
    """

    # 通过本地线程变量传递测试服务器地址信息
    if 'server' in process:
        localData.SERVER = process['server']

    tasks = process['tasks']
    users = process['users']

    variables = {}

    for task in tasks:
        # 获取用户ID
        user = task['user']

        if user not in variables:
            variables[user] = {}

        userVariable = variables[user]

        # 获取用户角色
        role = users[user]['role']
        module = sys.modules[role]

        # 获取用户行为
        action = task['action']
        actionName = action['name']
        func = getattr(module, actionName)

        # 处理输入参数
        param = copy.deepcopy(action['param'])
        for k, v in param.items():
            if v.startswith('{{'):

                vs = v[2:-2].split('.')
                if len(vs) > 1:

                    vas = variables[vs[0]]
                    if vs[1] in vas:
                        param[k] = vas[vs[1]]
                    else:
                        param[k] = None

                else:

                    vas = userVariable
                    if vs[0] in vas:
                        param[k] = vas[vs[0]]
                    else:
                        param[k] = None

        # 执行动作
        task['result'] = {}
        res = apply(func, [], param)

        for v in res.outMap:
            for k in v:
                task['result'][k] = v[k]

        # 参数提取
        if (res is not None) and ('extract' in action):
            for k, v in action['extract'].items():
                userVariable[v] = res[k]

        # 参数校验
        if (res is not None) and 'expect' in action:
            for k, v in action['expect'].items():
                val = res[k]

                # 处理期望值不相等的异常
                if val != str(v):
                    task['exception'] = k + '=' + str(val)
                    return process

        task['variables'] = copy.deepcopy(userVariable)

    return process
