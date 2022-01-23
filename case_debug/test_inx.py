import pytest
import requests
from common.requesthandler import RequestHandler
from common.operationExcel import OperationExcel
import allure

'''跳过模块内所有测试用例'''
# pytestmark =pytest.mark.skip("no reason")
requests.packages.urllib3.disable_warnings()

excel_obj = OperationExcel(2, 'data_debug', 'inx-1.xls')
smokecaselist = excel_obj.casesmoke()
smokecasenamelist = []
for i in smokecaselist:
    smokecasenamelist.append(i['描述'])


@allure.feature("测试somke用例")
@pytest.mark.parametrize("smoke", smokecaselist, ids=smokecasenamelist)
def test_01(smoke, pytestconfig, login_local_primary_market):
    case = RequestHandler(smoke, "data_debug", "inx_test.json")
    result = case.send_request(pytestconfig, login_local_primary_market, 1)
    case.result_handle(result)
    case.assert_handle(result)


if __name__ == "__main__":
    # pytest.main(['--alluredir', './report/report.html'])
    # # 执行命令 allure generate ./temp -o ./report --clean ，生成测试报告
    # os.system('allure generate ./report/report.html -o ./report --clean')
    pytest.main(['-s', 'test_inx.py'])
    # pytest.main(['-s', 'test_00.py','-m=smoke'])
    # pytest.main(['-s', 'test_00.py','-m=not smoke'])
