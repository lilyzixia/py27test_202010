''' 
author:紫夏
Time:2020/9/27 0:25
'''


import unittest
import os
import jsonpath
from decimal import Decimal
from library.myddt import ddt,data
from common.handle_excel import Handle_excel
from common.handle_path import DATA_DIR,BASE_DIR
from common.handleConfig import conf
from requests import request
from common.handler_log import log
from common.handle_db import Handle_db
from common.handle_data import EnvData,replace_data
from common.hanler_login import TestBase

@ddt
class TestRecharge(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATA_DIR,'cases.xlsx'),'recharge')
    cases=excel.read_data()
    db=Handle_db()

    @classmethod
    def setUpClass(cls):
        TestBase.login()
        # 准备登录的相关信息
        # url = conf.get('env', 'BASE_URL') + '/member/login'
        # data={
        #     'mobile_phone':conf.get('test_data','phone'),
        #     'pwd': conf.get('test_data', 'pwd'),
        # }
        # headers=eval(conf.get('env','headers'))
        # response=request(method='post',url=url,json=data,headers=headers)
        # res=response.json()
        # # cls.member_id=str(jsonpath.jsonpath(res,'$..id')[0])
        # # cls.token = 'Bearer'+' '+jsonpath.jsonpath(res, '$..token')[0]
        #
        # member_id=str(jsonpath.jsonpath(res,'$..id')[0])
        # setattr(EnvData,'member_id',member_id)
        # token = 'Bearer'+' '+jsonpath.jsonpath(res, '$..token')[0]
        # setattr(EnvData,'token',token)


        # print('提取到的member_id为',cls.member_id)
        # print('提取到的token为', cls.token)



    @data(*cases)
    def test_recharge(self,case):
        row=case['case_id']+1
        url=conf.get('env','BASE_URL')+case['url']
        method=case['method']
        expected=eval(case['expected'])
        # 准备用例数据
        # 替换用户Id
        # if '#member_id#' in case['data']:
             # case['data']=case['data'].replace('#member_id#',self.member_id)
        # data = eval(case['data'])
        data = eval(replace_data(case['data']))

        # 准备请求头
        headers=eval(conf.get('env','headers'))
        headers['Authorization']=getattr(EnvData,'token')

        # 判断该用例是否需要数据库校验
        if case['check_sql']:
            sql=case['check_sql'].format(getattr(EnvData,'member_id'))

            start_money=self.db.find_one(sql)['leave_amount']
            print('充值之前的金额',start_money)


        response=request(url=url,
                         method=method,
                         headers=headers,
                         json=data)
        res=response.json()
        print('预期结果',expected)
        print('实际结果',res)

        # 获取充值之后的账户余额
        if case['check_sql']:
            sql=case['check_sql'].format(getattr(EnvData,'member_id'))
            # sql=replace_data(case['check_sql'])
            end_money=self.db.find_one(sql)['leave_amount']
            print('充值之后的金额',end_money)


        try:
            self.assertEqual(res['code'],expected['code'])
            self.assertEqual(res['msg'],expected['msg'])
            # 判断是否需要进行sql校验
            if case['check_sql']:
                self.assertEqual(end_money-start_money,Decimal(str(data['amount'])))
        except AssertionError as e:

            self.excel.write_data(row=row, column=8, value='fail')
            log.error('用例--{}--执行未通过'.format(case['title']))
            log.exception(e)
            log.debug('预期结果:{}'.format(expected))
            log.debug('实际结果:{}'.format(res))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value='pass')
            log.info('用例--{}--执行通过'.format(case['title']))




