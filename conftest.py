import pytest
import requests

'''单独管理一些预置的操作场景，登录接口可以写入conftest文件中，并放入根目录，所有测试用例均可以调用 
    
   host/email 等可以放到配置文件中（在项目的根目录一般会放一个 pytest.ini 写一些配置参数）
   
   字典接口可以放到json参数文件
'''


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="type1", help="my option: type1 or type2"
    )
    # 添加参数到配置文件pytest.ini
    #type 是类型，默认None，可以设置：None, "pathlist", "args", "linelist", "bool"
    parser.addini('debug_url', type=None, default="https://api.apiopen.top/", help='测试环境域名')
    parser.addini('online_url', type=None, default="https://api.apiopen.top/", help='测试环境域名')
    parser.addini('account_id', type=None, default="fe2942fde37e51cdd77535649b70e621", help='个人账号id')
    parser.addini('vie_enterprise_id', type=None, default="fe2942fde37e51cdd77535649b70e621", help='境外企业ID')
    parser.addini('domestic_enterprise_advanced_id', type=None, default="fe2942fde37e51cdd77535649b70e621", help='境内企业一级市场高级版id')


@pytest.fixture(scope="session")
def login():
    #登录方法
    url = "https://test-server.inssent.net/inx/loosely/login"
    param = {"username":"15611360995","password":"{\"ct\":\"GeygVtDXGSF4Uv5sGCSRQA==\",\"iv\":\"5468697320697320616e204956343536\"}","type":1,"code":"","loginType":1}
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    r = requests.post(url, data=param, headers=header)
    token = r.json()['data']['token']
    return token


@pytest.fixture(scope="session")
def login_local_primary_market(pytestconfig, login):
    """该企业为境内公司，一级市场，高级版，更新token"""
    url = "https://test-server.inssent.net/inx/enterprise/choose"
    param = {"id": pytestconfig.getini("domestic_enterprise_advanced_id")}
    header = {
                    "X-ACCESS-E-KEY": pytestconfig.getini("account_id"),
                    "X-ACCESS-SIGN": "true",
                    "X-ACCESS-TOKEN": login
        }

    r = requests.post(url, data=param, headers=header)
    newtoken = r.json()['data']
    return newtoken


@pytest.fixture(scope="session")
def login_vie_primary_market(pytestconfig, login):
    """该企业为境外公司，一级市场，高级版，更新token"""
    url = "https://test-server.inssent.net/inx/enterprise/choose"
    param = {"id": pytestconfig.getini("vie_enterprise_id")}
    token = login

    header = {
                    "X-ACCESS-E-KEY": pytestconfig.getini("account_id"),
                    "X-ACCESS-SIGN": "true",
                    "X-ACCESS-TOKEN": token
        }

    r = requests.post(url, data=param, headers=header)
    newtoken = r.json()['data']
    return newtoken


def pytest_collection_modifyitems(items):
    """
    测试用例收集完成时，将收集到的item的name和nodeid的中文显示在控制台上
    :return:
    """
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode_escape")
        print(item.nodeid)
        item._nodeid = item.nodeid.encode("utf-8").decode("unicode_escape")


# if __name__ == "__main__":
#     pytest.main("-s","conftest.py")