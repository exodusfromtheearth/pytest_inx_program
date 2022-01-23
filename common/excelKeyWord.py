# -*- coding: utf-8 -*-
# Author:xtgao
# Filename:excelKeyWord.py
# Time:2021/1/19 6:16 下午


class TestCaseKeyWord:
    """
    定义测试用例关键字类
    """
    case_id = 0
    case_name = 1
    url = 2
    method = 3
    header = 4
    data = 5
    case_depend = 6
    """case依赖"""
    case_depend_data = 7
    """依赖的返回数据"""
    field_depend = 8
    """数据依赖字段"""
    expect = 9
    json_expect = 10
    expect_status_code = 11
    is_execute = 12
    smoke = 13
    result = 14
