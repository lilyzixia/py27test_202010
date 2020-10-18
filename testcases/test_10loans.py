''' 
author:紫夏
Time:2020/10/12 22:50
'''
import unittest
import os
from library.myddt import ddt,data
from common.handle_excel import Handle_excel
from common.handle_path import DATA_DIR
from common.hanler_login import TestBase
from common.handle_data import EnvData,replace_data
from common.handleConfig import conf
from requests import request
from common.handler_log import log


@ddt
class TestLoans(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATA_DIR,'cases.xlsx'),'loans')
    cases=excel.read_data()

    # @classmethod
    # def setUpClass(cls):
    #     TestBase.login()

    @data(*cases)
    def test_loans(self,case):
        expected=eval(case['expected'])
        url=conf.get('env','BASE_URL')+case['url']
        method=case['method']
        data=eval(case['data'])
        headers=eval(conf.get('env','headers'))
        # headers['Authorization'] = getattr(EnvData, 'token')
        row=case['case_id']+1
        response=request(method=method,url=url,headers=headers,params=data)
        res=response.json()

        print('实际结果：',res)
        print('预期结果：',expected)

        try:
            self.assertEqual(res['code'], expected['code'])
            self.assertEqual(res['msg'], expected['msg'])
            # 校验返回数据条数是否和预期一致
            self.assertEqual(len(res['data']),expected['len'])
        except AssertionError as e:
            log.error('__测试案例{}__测试不通过_'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row=row,column=8,value='fail')
            log.debug('实际结果：',res)
            log.debug('预期结果：',expected)
            raise e
        else:
            self.excel.write_data(row=row,column=8,value='pass')








