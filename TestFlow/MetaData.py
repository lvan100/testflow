#!/usr/bin/python
# -*- coding: UTF-8 -*-

import FlatMap

"""
角色列表，数据格式如下：
[
    {
        "id":"<role>",
        "name":"<name>"
    }
]
"""
ROLELIST = []

"""
服务的元数据列表，数据格式如下:
{
    "<role>":{
        "<action>":{
            "name":"<动作名称>",
            "description":"<动作描述>",
            "param":{
              "<phone>":{
                "tip":"<参数描述>",
                "default":"<默认值>"
              }
            },
            "extract":{
              "<$.p1.p2>": "<新的变量名称>"
            }
        }
    }
}
"""
METADATA = {}

"""
角色的行为列表
{
    "<role>":[
        {
            "name":"<动作名称>",
            "description":"<动作描述>"
        },
        {
            "group":{
                "tag":"<分组标签>",
                "actions":[
                    {
                        "name":"<动作名称>",
                        "description":"<动作描述>"
                    }
                ]
            }
        }
    ]
}
"""
ACTIONLIST = {}


# 获取角色列表信息
def roleList():
    return ROLELIST


# 获取所有元数据信息
def metaData():
    return METADATA


# 获取角色的行为列表
def actionList(role):
    return ACTIONLIST[role]


# 获取角色行为的详细信息
def actionInfo(role, action):
    return METADATA[role][action]


def _getRole(func):
    """
    获取函数所在的角色
    :param func: 注册函数
    :return: 返回角色ID
    """

    return func.func_globals['__name__']


def role(name):
    """
    装饰器函数，注册角色
    """

    def decorator(func):
        ROLELIST.append({
            "name": name,
            "id": _getRole(func)
        })
        return func

    return decorator


def action(description, param, group=None, extract=None):
    """
    装饰器函数，注册服务的元数据信息
    @description 动作描述
    @param 动作参数,形式:
            {
              "<phone>":{
                "tip":"<参数描述>",
                "default":"<默认值>"
              }
            }
    @group 服务分组
    @extract 结果提取，形式:
            {
              "<$.p1.p2>": "<px>"
            }
    """

    def decorator(func):
        # 获取角色名称
        _role = _getRole(func)

        if _role not in METADATA:
            METADATA[_role] = {}
            ACTIONLIST[_role] = []

        # 获取行为名称
        actionName = func.func_name

        # 获取行为列表
        actionList = ACTIONLIST[_role]

        thisAction = {
            'name': actionName,
            'description': description
        }

        METADATA[_role][actionName] = {
            "name": actionName,
            "description": description,
            "param": param,
            "extract": extract
        }

        found = False

        # 查找分组
        for _action in actionList:
            if "group" in _action:
                node = _action["group"]
                if node["tag"] == group:
                    node["actions"].append(thisAction)
                    found = True
                    break

        if not found:
            if group is None:
                actionList.append(thisAction)
            else:
                # 构建新的分组
                actionList.append({
                    "group": {
                        "tag": group,
                        "actions": [thisAction]
                    }
                })

        # 使函数返回值扁平化
        def invoker(*args, **kwargs):
            _result = func(*args, **kwargs)
            return FlatMap.toFlatMap(_result)

        return invoker

    return decorator
