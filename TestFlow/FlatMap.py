#!/usr/bin/python
# -*- coding: UTF-8 -*-

import io
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FlatMap:
    """
    封装扁平化的对象
    """

    def __init__(self, obj):
        """
        构造函数
        :param obj: 原始对象
        """

        self.obj = obj
        self.outMap = []

    def __getitem__(self, item):
        """
        获取被封装对象的属性
        :param item: 属性名
        :return: 属性值，找不到返回 None。
        """

        if not isinstance(item, str):
            return None

        if not item.startswith("$"):
            item = "$." + item

        for val in self.outMap:
            if item in val:
                return val[item]

        return None

    def __str__(self):
        """ toString() """

        with io.StringIO() as output:
            for val in self.outMap:
                if isinstance(val, str):
                    output.write(val + u"\n")
                else:
                    for k in val:
                        output.write(k + u"=" + val[k] + u"\n")
            return output.getvalue()[:-1]


def toFlatMap(obj):
    """ 对象扁平化 """

    _1 = FlatMap(obj)
    _toFlatMap(_1.outMap, obj)
    return _1


def _toFlatMap(outMap, obj, prefix=None):
    """ 对象扁平化 """

    if isinstance(obj, (str, unicode, int, long, float, bool, complex)):
        if prefix is None:
            outMap.append({"$": str(obj)})
        else:
            outMap.append({prefix[:-1]: str(obj)})

    elif isinstance(obj, (list, tuple, set)):
        if prefix is None:
            prefix = "$."
        else:
            outMap.append({prefix[:-1]: "[]"})

        for i, v in enumerate(obj):
            _toFlatMap(outMap, v, prefix[:-1] + "[" + str(i) + "].")

    elif isinstance(obj, dict):
        if prefix is None:
            prefix = "$."
        else:
            outMap.append({prefix[:-1]: "{}"})

        for k in obj:
            _toFlatMap(outMap, obj[k], prefix + k + ".")

    else:
        print("error type " + str(type(obj)))
        exit(0)


if __name__ == '__main__':
    """"""

    print(toFlatMap(True))
    print(toFlatMap(3 + 5j))
    print(toFlatMap(3))
    print(toFlatMap(5L))
    print(toFlatMap("a"))
    print(toFlatMap(["a", "b"]))
    print(toFlatMap(("a", "b")))
    print(toFlatMap({"a", "b", "a"}))
    print(toFlatMap({"a": "b"}))
    print(toFlatMap("中国"))

    flatMap = toFlatMap({
        "a": {
            "b": {
                "c": "d",
                "e": [{"f": {"h": "i"}}, "g"],
                "j": 6
            }
        }
    })
    print(flatMap)

    print(flatMap["$."])
    print(flatMap["a"])
    print(flatMap["$.a.b"])
    print(flatMap["a.b.c"])
