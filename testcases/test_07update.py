''' 
author:紫夏
Time:2020/10/7 22:30
'''
import unittest
import os
from requests import request
from common.handle_excel import Handle_excel
from common.handle_path import DATA_DIR
from library.myddt import ddt,data
from common.handleConfig import conf
from jsonpath import jsonpath
from common.handle_db import Handle_db
from common.handler_log import log
from common.hanler_login import TestBase
from common.handle_data import EnvData,replace_data

@ddt
class TestUpdate(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATA_DIR,'cases.xlsx'),'update')
    cases=excel.read_data()
    db=Handle_db()

    @classmethod
    def setUpClass(cls):
        TestBase.login()
        # headers=eval(conf.get('env','headers'))
        # url=conf.get('env','BASE_URL')+'/member/login'
        # data={
        #     "mobile_phone": conf.get('test_data', 'phone'),
        #     "pwd": conf.get('test_data', 'pwd')
        # }
        # response=request(method='post',url=url,headers=headers,json=data)
        # res=response.json()
        # cls.member_id=str(jsonpath(res,'$..id')[0])
        # cls.token='Bearer '+jsonpath(res,'$..token')[0]

    @data(*cases)
    def test_update(self,case):

        expected=eval(case['expected'])
        if '#member_id#' in case['data']:
            case['data']=case['data'].replace('#member_id#',getattr(EnvData,'member_id'))
        data=eval(case['data'])
        headers=eval(conf.get('env','headers'))
        headers['Authorization']=getattr(EnvData,'token')
        row=case['case_id']+1
        method=case['method']
        url=conf.get('env','BASE_URL')+case['url']

        response=request(method=method,url=url,headers=headers,json=data)
        res=response.json()

        if case["check_sql"]:
            sql=replace_data(case['check_sql'])
            second_name=self.db.find_one(sql)['reg_name']
            print('改昵称后的昵称:',second_name)


        print('预期结果', expected)
        print('实际结果', res)

        try:
            self.assertEqual(res['code'], expected['code'])
            self.assertEqual(res['msg'], expected['msg'])
            if case["check_sql"]:
                self.assertEqual(second_name,data['reg_name'])

        except AssertionError as e :
            log.error('测试用例---{}---测试不通过'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row=row,column=8,value='fail')
            log.debug('预期结果',expected)
            log.debug('实际结果',res)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value='pass')
            log.error('测试用例---{}---测试通过'.format(case['title']))