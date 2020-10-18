''' 
author:紫夏
Time:2020/10/7 17:03
'''

import unittest
import os
from decimal import Decimal
from jsonpath import jsonpath
from requests import request
from library.myddt import ddt,data
from common.handle_excel import Handle_excel
from common.handle_path import DATA_DIR
from common.handleConfig import conf
from common.handle_db import Handle_db
from  common.handler_log import log
from common.hanler_login import TestBase
from common.handle_data import EnvData,replace_data

@ddt
class TestWithdraw(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATA_DIR,'cases.xlsx'),'withdraw')
    cases=excel.read_data()
    db=Handle_db()


    @classmethod
    def setUpClass(cls):
        TestBase.login()
        # data={
        #     "mobile_phone":conf.get('test_data','phone'),
        #     "pwd":conf.get('test_data','pwd')
        # }
        #
        # url=conf.get('env','BASE_URL')+'/member/login'
        # # 要eval脱除
        # headers=eval(conf.get('env','headers'))
        # response=request(method='post',url=url,headers=headers,json=data)
        # res=response.json()
        # cls.member_id=str(jsonpath(res,'$..id')[0])
        # cls.token='Bearer '+jsonpath(res,'$..token')[0]


    @data(*cases)
    def test_withdraw(self,case):
        # 测试数据需要去除参数化
        # if '#member_id#' in case['data']:
        #     case['data']=case['data'].replace('#member_id#',)
        data=eval(replace_data(case['data']))
        expected=eval(case['expected'])
        method=case['method']
        url=conf.get('env','BASE_URL')+case['url']
        # 请求头要eval
        headers=eval(conf.get('env','headers'))
        headers['Authorization']=getattr(EnvData,'token')
        row=case['case_id']+1

        if case['check_sql']:
            sql=replace_data(case['check_sql'])
            start_money=self.db.find_one(sql)['leave_amount']
            print('提现之前的余额:',start_money)


        response=request(method=method,url=url,headers=headers,json=data)
        res = response.json()
        print('预期结果：',expected)
        print('实际结果：',res)

        if  case['check_sql']:
            sql=replace_data(case['check_sql'])
            end_money=self.db.find_one(sql)['leave_amount']
            print('提现之后的余额:',end_money)

        try:
            self.assertEqual(res['code'],expected['code'])
            self.assertEqual(res['msg'],expected['msg'])
            if case['check_sql']:
                # Decimal需要使用str修饰
                # 金额不是在case里面，是在data里面的amount
                self.assertEqual(start_money-end_money,Decimal(str(data['amount'])))
        except AssertionError as e:
            log.error('测试———{}—————执行未通过'.format(case['title']))
            log.debug('预期结果：{}'.format(expected))
            log.debug('实际结果：',res)
            log.exception(e)
            self.excel.write_data(row=row,column=8,value='fail')
            raise e
        else:
            self.excel.write_data(row=row, column=8, value='pass')
            log.info('测试———{}—————执行通过'.format(case['title']))
