''' 
author:紫夏
Time:2020/9/18 1:48
'''


import unittest
from common.handle_excel import Handle_excel
from library.myddt import ddt,data
from common.handleConfig import conf
from requests import request
from  common.handler_log import log
from common.handle_path import DATA_DIR
import os

# filename = r'F:\python37test\20200917APITEST\data\cases.xlsx'
filename = os.path.join(DATA_DIR,'cases.xlsx')

@ddt
class LoginTest(unittest.TestCase):
    excel=Handle_excel(filename,'login')
    cases=excel.read_data()

    @data(*cases)
    def test_login(self,case):
        # pass
        method=case['method']
        row=case['case_id']+1
        url='http://api.lemonban.com/futureloan'+case['url']
        data=eval(case['data'])
        expected=eval(case['expected'])
        headers=eval(conf.get('env','headers'))
        response=request(method=method,json=data,headers=headers,url=url)
        res=response.json()

        # print('预期结果',expected)
        # print('实际结果',res)

        try:
            self.assertEqual(expected['msg'],res['msg'])
            self.assertEqual(expected['code'],res['code'])
        except AssertionError as e:
            self.excel.write_data(row=row,column=8,value='fail')
            log.error('用例--{}--执行未通过'.format(case['title']))
            log.exception(e)
            log.debug('预期结果:{}'.format(expected))
            log.debug('实际结果:{}'.format(res))
            raise e
        else:
            self.excel.write_data(row=row, column=8, value='pass')
            log.info('用例--{}--执行通过'.format(case['title']))


