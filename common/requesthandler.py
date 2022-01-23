import pytest
import json

from common.operationJson import depend_list, read_json_file, write_json_file, depend_data_replace
from common.requestmethod import req
from common.operationExcel import OperationExcel, ExcelVariables
from common.asserthandler import value_assert
from common.logger import atp_log
from xlutils.copy import copy
from common.filepublic import filepath
from common.excelKeyWord import TestCaseKeyWord


class RequestHandler:
    def __init__(self, case, jsonpath, json_filename):
        self.case = case
        # 读取json文件取出已有的参数
        self.json_name = json_filename
        self.json_path = jsonpath
        self.load_dict = read_json_file(self.json_path, self.json_name)

    def check_url(self):
        # 第一步 处理URL-----------------------------------------------------------------------
        """
        @param value:   测试用例集
        @param host :   因为可能存在多个域名
        @param pytestconfig: 内置 fixture
        """
        # # 替换url中的参数
        url = depend_data_replace(self.case[ExcelVariables.url], self.load_dict)
        return url

    def check_param(self):
        # 第二步 处理参数  待处理随机数------------------------------------------------------------------
        params = self.case[ExcelVariables.params]
        if len(str(params).strip()) == 0:
            pass
        elif len(str(params).strip()) > 0:
            if isinstance(params, dict):
                params = json.dumps(params, ensure_ascii=False)
            else:
                pass
        params = depend_data_replace(params, self.load_dict)
        params = params.encode("utf-8")
        return params

    def send_request(self, pytestconfig, token, enterprise_type):
        """第三步：发送请求"""
        method = self.case[ExcelVariables.method]
        params = self.check_param()
        '''判断测试环境还是发布环境'''
        if enterprise_type == 1:
            url = pytestconfig.getini('debug_url') + self.check_url()
            key = pytestconfig.getini("account_id") + pytestconfig.getini("domestic_enterprise_advanced_id")
        elif enterprise_type == 2:
            url = pytestconfig.getini('debug_url') + self.check_url()
            key = pytestconfig.getini("account_id") + pytestconfig.getini("vie_enterprise_advanced_id")
        else:
            url = pytestconfig.getini('online_url') + self.check_url()
            key = "f4047c56066ca7cac42c1c7093e831bfed978da8517bf0db4257f9ee3b494695"

        header = {
            "X-ACCESS-E-KEY": key,
            "X-ACCESS-SIGN": "true",
            "X-ACCESS-TOKEN": token
        }
        atp_log.info(url)
        r = req.request(url=url, headers=header, data=params, method=method, verify=False)
        result = r.json()
        return result

    """处理返回结果"""
    def result_handle(self,result):
        # 第四步 处理返回结果,写入json文件-------------------------------------------------------------------
        # 1/依赖返回数据,   2/依赖返回key值
        dep_data = self.case[ExcelVariables.depend_data]
        dep_key = self.case[ExcelVariables.depend_key]
        if dep_key:
            # 输出之后是这样的格式[{'amount_level_id': 99, 'amount_level_name': '待定'}],把depend_dcit存到json文件中
            load_dict2 = depend_list(dep_data, dep_key, result)
            write_json_file(self.json_path, self.json_name, load_dict2)

    def assert_handle(self,result):
        """第五步：断言"""
        assert_value = self.case[ExcelVariables.expect]
        assert_json = self.case[ExcelVariables.json_expect]
        assert_code = self.case[ExcelVariables.expect_status_code]
        assert result['errno'] == assert_code, "返回状态码不对"
        value_assert(result, assert_value, assert_json)


# if __name__ == "__main__":
#     # obj = TestOrg()
#     pytest.main(['-s', 'test_03_funding.py'])
