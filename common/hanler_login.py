''' 
author:紫夏
Time:2020/10/11 18:50
'''


from requests import request
from jsonpath import jsonpath
from common.handle_data import EnvData
from common.handleConfig import conf


class TestBase:
    # 封装成静态方法
    @staticmethod
    def login():
        # 准备登录的相关信息
        url = conf.get('env', 'BASE_URL') + '/member/login'
        data={
            'mobile_phone':conf.get('test_data','phone'),
            'pwd': conf.get('test_data', 'pwd'),
        }
        headers=eval(conf.get('env','headers'))
        response=request(method='post',url=url,json=data,headers=headers)
        res=response.json()

        member_id=str(jsonpath(res,'$..id')[0])
        setattr(EnvData,'member_id',member_id)
        token = 'Bearer'+' '+jsonpath(res, '$..token')[0]
        setattr(EnvData,'token',token)

    @staticmethod
    def admin_login():
        # 准备登录的相关信息
        url = conf.get('env', 'BASE_URL') + '/member/login'
        data={
            'mobile_phone':conf.get('test_data','admin_phone'),
            'pwd': conf.get('test_data', 'admin_pwd'),
        }
        headers=eval(conf.get('env','headers'))
        response=request(method='post',url=url,json=data,headers=headers)
        res=response.json()

        # admin_member_id=str(jsonpath(res,'$..id')[0])
        # setattr(EnvData,'member_id',admin_member_id)
        admin_token = 'Bearer'+' '+jsonpath(res, '$..token')[0]
        setattr(EnvData,'admin_token',admin_token)

    @staticmethod
    def invest_login():
        # 准备登录的相关信息
        url = conf.get('env', 'BASE_URL') + '/member/login'
        data={
            'mobile_phone':conf.get('test_data','invest_phone'),
            'pwd': conf.get('test_data', 'invest_pwd'),
        }
        headers=eval(conf.get('env','headers'))
        response=request(method='post',url=url,json=data,headers=headers)
        res=response.json()

        invest_member_id=str(jsonpath(res,'$..id')[0])
        setattr(EnvData,'member_id',invest_member_id)
        invest_token = 'Bearer'+' '+jsonpath(res, '$..token')[0]
        setattr(EnvData,'token',invest_token)