

urllist = ["https://test-server.inssent.net/inx/message/links",
         "https://test-server.inssent.net/inx/help/menuList?type=1"
        ]


# @pytest.mark.parametrize("url",urllist)
# def test01(url,login):
#     '''测试首页接口'''
#     token = login
#     # url = "https://test-server.inssent.net/inx/message/links"
#     header = {
#         "X-ACCESS-E-KEY": "f4047c56066ca7cac42c1c7093e831bf",
#         "X-ACCESS-SIGN": "true",
#         "X-ACCESS-TOKEN": token
#     }
#     r = requests.get(url,headers=header)
#     result = r.json()
#     print(result)