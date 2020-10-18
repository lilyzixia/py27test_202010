''' 
author:紫夏
Time:2020/10/8 16:24
'''

import unittest
import os
from common.handle_excel import Handle_excel
from common.handle_path import DATA_DIR
from library.myddt import ddt,data
from common.handleConfig import conf
from requests import request
from jsonpath import jsonpath
from common.handle_db import Handle_db
from common.handler_log import log
from common.hanler_login import TestBase
from common.handle_data import EnvData,replace_data

@ddt
class TestAudit(unittest.TestCase):
    excel = Handle_excel(os.path.join(DATA_DIR,'cases.xlsx'),'audit')
    cases=excel.read_data()
    db=Handle_db()

    @classmethod
    def setUpClass(cls):
        TestBase.login()
        TestBase.admin_login()
    #     headers=eval(conf.get('env','headers'))
    #     url=conf.get('env','BASE_URL')+'/member/login'
    #
    # #     1.管理员登陆
    #
    #     admin_data={
    #         'mobile_phone':conf.get('test_data','admin_phone'),
    #         'pwd':conf.get('test_data','admin_pwd'),
    #     }
    #
    #     response1 = request(url=url, json=admin_data, headers=headers, method='post')
    #     res1 = response1.json()
    #     cls.admin_token='Bearer '+jsonpath(res1,'$..token')[0]

    #     2.普通用户登陆
    #     user_data = {
    #     'mobile_phone': conf.get('test_data', 'phone'),
    #     'pwd': conf.get('test_data', 'pwd'),
    # }
    #     response2 = request(url=url, json=user_data, headers=headers, method='post')
    #     res2 = response2.json()
    #     cls.user_token = 'Bearer ' + jsonpath(res1, '$..token')[0]
    #     cls.user_member_id =  jsonpath(res1, '$..id')[0]

        # print('用户id',cls.user_member_id)
        # print('用户token',cls.user_token)
        # print('管理员token',cls.admin_token)

        # print('用户id',getattr(EnvData,'member_id'))
        # print('用户token',getattr(EnvData,'token'))
        # print('管理员token',getattr(EnvData,'admin_token'))


    # 加标
    def setUp(self):
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = getattr(EnvData,'token')
        data = {"member_id":getattr(EnvData,'member_id'),
             "title":"贷款买房1",
             "amount":1000,
             "loan_rate":1,
             "loan_term":1,
             "loan_date_type":1,
             "bidding_days":1}
        url = conf.get('env', 'BASE_URL') + '/loan/add'
        response3 = request(url=url, json=data, headers=headers, method='post')
        res3 = response3.json()
        loan_id =  str(jsonpath(res3, '$..id')[0])
        setattr(EnvData,'loan_id',loan_id)

        # print('标id', getattr(EnvData,'loan_id'))


    @data(*cases)
    def test_audit(self,case):

        url = conf.get('env', 'BASE_URL') + case['url']
        expected = eval(case['expected'])

        # 判断是否需要替换审核通过的id
        # if '#pass_loan_id#' in case['data']:
        #     # 将之前保存的审核通过的标Id替换到测试用例中
        #     case['data']=replace_data(case['data'])
        #     print(case['data'])

        # data = eval(case['data'].replace('#loan_id#',str(self.loan_id)))
        # case['data']=replace_data(case['data'])
        # if '#loan_id#' in case['data']:

        data = eval(replace_data(case['data']))
        method=case['method']
        row=case['case_id']+1
        headers = eval(conf.get('env', 'headers'))
        headers['Authorization'] = getattr(EnvData,'admin_token')

        if case['title'] == '普通用户审核' :
            headers['Authorization'] = getattr(EnvData,'token')

        response4 = request(url=url, json=data, headers=headers, method=method)
        res4 = response4.json()

        print('实际结果',res4)

        # 判断是否是审核通过的案例并且审核成功
        if case['title']=='审核通过' and expected['msg']=='OK':
            # 将执行通过的标ID保存为类属性
            pass_loan_id=str(data['loan_id'])
            setattr(EnvData,'pass_loan_id',pass_loan_id)

        try:
            self.assertEqual(res4['code'], expected['code'])
            self.assertEqual(res4['msg'], expected['msg'])

            if case['check_sql']:
                sql = replace_data(case['check_sql'])
                # sql = case['check_sql'].replace('#loan_id#', str(self.loan_id))
                end_status = self.db.find_one(sql)['status']
                print('加标后的状态:', end_status)
                self.assertEquals(expected['status'], end_status)


        except AssertionError as e:
            log.debug('预期结果：', expected)
            log.debug('实际结果：', res4)
            log.error('测试用例--{}--测试不通过'.format(case['title']))
            log.exception(e)
            self.excel.write_data(row=row, column=8, value='fail')
            raise e
        else:
            self.excel.write_data(row=row, column=8, value='pass')
            log.error('测试用例--{}--测试通过'.format(case['title']))
