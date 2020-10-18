''' 
author:紫夏
Time:2020/10/18 1:03
'''

import os
import unittest
from library.myddt import ddt,data
from common.handle_path import DATA_DIR
from common.handle_excel import Handle_excel
from random import randint
from common.handle_db import Handle_db
from common.handleConfig import conf
from requests import request
from common.handle_data import EnvData,replace_data
from jsonpath import jsonpath
from common.handler_log import log


@ddt
class TestMain(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATA_DIR,'cases.xlsx'),'main_stream')
    cases=excel.read_data()
    db=Handle_db()

    @data(*cases)
    def test_main(self,case):
        method = case['method']
        if '#member_id#' in case['url']:
            case['url'] = replace_data(case['url'])
        url = 'http://api.lemonban.com/futureloan' + case['url']
        row = case['case_id'] + 1
        # 替换手机号码
        if '#mobile_phone#' in case['data']:
            if case['interface'] == 'register':
                mobile_phone = self.random_phone()
                setattr(EnvData,'mobile_phone',mobile_phone)
                # case['data'] = case['data'].replace('#mobile_phone#', mobile_phone)
                case['data'] = replace_data(case['data'])

                print(mobile_phone)
            else:
                # mobile_phone=getattr(EnvData,'mobile_phone')
                case['data'] = replace_data(case['data'])


        data = eval(replace_data(case['data']))
        print(data)
        expected=eval(case['expected'])

        headers = eval(conf.get('env', 'headers'))
        if  case['interface'] != 'register'   and  case['interface'] != 'login'  :
            headers['Authorization'] = getattr(EnvData, 'token')
        # elif case['interface'] != 'login':
        #     headers['Authorization'] = getattr(EnvData, 'token')


        response=request(method=method,url=url,json=data,headers=headers)
        res=response.json()

        print('预期结果：',expected)
        print('实际结果：',res)

        if case['interface'] == 'login':
            member_id=str(jsonpath(res,'$..id')[0])
            token='Bearer '+jsonpath(res,'$..token')[0]
            setattr(EnvData,'member_id',member_id)
            setattr(EnvData, 'token', token)

        if case['interface'] == 'add':
            loan_id = str(jsonpath(res, '$..id')[0])
            setattr(EnvData, 'loan_id', loan_id)


        try:
            self.assertEqual(expected['code'],res['code'])
            self.assertEqual(expected['msg'],res['msg'])

        except AssertionError as e:
            log.debug('预期结果：',expected)
            log.debug('实际结果：',res)
            log.error('测试用例--{}--测试不通过'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row= row,column=8,value='fail')
            raise e
        else:
            self.excel.write_data(row=row, column=8, value='pass')
            log.error('测试用例--{}--测试通过'.format(case['title']))

    @classmethod
    def random_phone(cls):
        while True:
            phone='137'
            for i in range(8):
                r=randint(0,9)
                phone=phone+str(r)
            sql='select * from futureloan.member where mobile_phone={}; '.format(phone)
            res=cls.db.count(sql)
            if res==0:
                return phone


