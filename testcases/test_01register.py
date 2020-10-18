''' 
author:紫夏
Time:2020/9/17 21:56
'''

import unittest
import requests
import random
from common.handle_excel import Handle_excel
from library.myddt import ddt,data
from common.handleConfig import conf
from common.handler_log import log
import os
from common.handle_path import DATA_DIR
from common.handle_db import Handle_db

filename = os.path.join(DATA_DIR,'cases.xlsx')

@ddt
class RegisterTestCase(unittest.TestCase):
    excel=Handle_excel(filename,'register')
    cases=excel.read_data()
    db=Handle_db()



    @data(*cases)
    def test_register(self,case):
        # pass
        method=case['method']
        url='http://api.lemonban.com/futureloan'+case['url']
        row = case['case_id'] + 1
        # 替换手机号码
        if '#phone#' in case['data']:
            phone=self.random_phone()
            case['data']=case['data'].replace('#phone#',phone)

        data=eval(case['data'])
        expected=eval(case['expected'])
        headers=eval(conf.get('env','headers'))

        response=requests.request(method=method,url=url,headers=headers,json=data)
        res=response.json()
        # print('结果是',res)

        # print('预期结果', expected)
        # print('实际结果', res)

        try:
            self.assertEqual(res['code'],expected['code'])
            self.assertEqual(res['msg'],expected['msg'])
            # 判断是否需要进行sql校验
            if case['check_sql'] :
                sql=case['check_sql'].replace('#phone#',data['mobile_phone'])
                # res=self.db.find_one(sql)
                # self.db.close()
                # 判断是否有数据
                # self.assertTrue(res)

                res2=self.db.count(sql)
                self.assertEqual(1,res2)
                # self.db.close()

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

    @classmethod
    def random_phone(cls):
        while True:
            phone = '155'
            for i in range(8):
                r = random.randint(0, 9)
                phone += str(r)
            sql = 'select * from futureloan.member where mobile_phone={};'.format(phone)
            res = cls.db.count(sql)
            if res == 0:
                return phone

