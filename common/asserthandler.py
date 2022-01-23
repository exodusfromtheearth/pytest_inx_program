# -*- coding: utf-8 -*-
# Author:xtgao
# Filename:asserthandler.py
# Time:2021/1/19 7:00 下午
import json

import jsonpath
from pytest_assume.plugin import assume

"""设置断言，状态码如果不正确会继续对期望结果断言；
但是如果期望结果第一个断言失败，将不会继续断言后面的期望结果"""


def value_assert(result, assert_value, json_assert_value):
    try:
        """判断json结果断言是否为空"""
        if json_assert_value:
            json_assert_list = json_assert_value.split(",")
            r_list = []
            for m in json_assert_list:
                item = jsonpath.jsonpath(result, m)
                r_list.append(item)
            '''期望结果与jsonpath返回的结果一致'''
            assert_list = assert_value.split(",")
            j_list = []
            for n in assert_list:
                j_list.append(n)
            with assume: assert r_list == j_list, "json断言失败%s" % json_assert_value
        else:
            if assert_value:
                for i in assert_value:
                    with assume: assert i in json.dumps(result, ensure_ascii=False), "断言失败%s" % result
    except Exception as e:
        print("无法断言%s" % e)


def mysql_assert():
    try:
        pass
    except Exception as e:
        print("无法断言%s" % e)
