''' 
author:紫夏
Time:2020/10/8 15:05
'''
import os
import unittest
from library.myddt import ddt,data
from common.handle_path import DATA_DIR
from common.handleConfig import conf
from common.handle_excel import Handle_excel
from requests import request
from common.handler_log import log
from common.handle_db import Handle_db
from common.handle_data import EnvData,replace_data
from common.hanler_login import TestBase

@ddt
class TestAdd(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATA_DIR,"cases.xlsx"),'add')
    cases=excel.read_data()
    db=Handle_db()

    @classmethod
    def setUpClass(cls):
        TestBase.login()
        # headers=eval(conf.get('env','headers'))
        # data={
        #     'mobile_phone':conf.get('test_data','phone'),
        #     'pwd':conf.get('test_data','pwd'),
        # }
        # url=conf.get('env','BASE_URL')+'/member/login'
        # response=request(url=url,json=data,headers=headers,method='post')
        # res=response.json()
        #
        # # cls.member_id=str(jsonpath(res,'$..id')[0])
        # # cls.token='Bearer '+jsonpath(res,'$..token')[0]
        #
        # # 将提取出来的数据保存在EnvData （环境变量）
        # member_id=str(jsonpath(res,'$..id')[0])
        # setattr(EnvData,'member_id',member_id)
        # token='Bearer '+jsonpath(res,'$..token')[0]
        # setattr(EnvData,'token',token)


    @data(*cases)
    def test_add(self,case):
        headers = eval(conf.get('env', 'headers'))
        expected=eval(case['expected'])
        headers['Authorization']=getattr(EnvData,'token')
        # if '#member_id#' in case['data']:
            # case['data']=case['data'].replace('#member_id#',self.member_id)

            # 替换用例中的动态数据
            # case['data']=replace_data(case['data'])
        # data=eval(case['data'])
        # case['data']=
        data = eval(replace_data(case['data']))

        url = conf.get('env', 'BASE_URL') + case['url']
        method=case['method']
        row=case['case_id']+1

        if case["check_sql"]:
            # sql= case['check_sql'].replace('#member_id#', self.member_id)
            sql=replace_data(case["check_sql"])
            start_count=self.db.count(sql)
            print('加标前的数量:',start_count)

        response = request(url=url, json=data, headers=headers, method=method)
        res = response.json()


        print('预期结果：',expected)
        print('实际结果：',res)



        try:
            self.assertEqual(res['code'],expected['code'])
            self.assertEqual(res['msg'],expected['msg'])
            if case['check_sql']:
                # sql = case['check_sql'].replace('#member_id#', self.member_id)
                sql =replace_data(case['check_sql'])
                end_count = self.db.count(sql)

                print('加标后的数量:', end_count)
                self.assertEquals(1,end_count-start_count)


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

