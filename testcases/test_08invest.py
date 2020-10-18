''' 
author:紫夏
Time:2020/10/11 17:20
'''
'''
投资：
1.有可以投资的项目
    创建项目——借款人（普通用户）登录：2个请求 登录id+token+标id
    审核通过——管理员登录：2个请求  管理员id+token
    
2.投资用户有钱
    投资人（普通用户）登陆：1个请求  投资id+token
    投资人充值：1个请求

3.执行投资相关的用例


'''



import unittest
import os
from jsonpath import jsonpath
from requests import request
from library.myddt import ddt,data
from common.handle_excel import Handle_excel
from common.handle_path import DATA_DIR
from common.handleConfig import conf
from common.handle_data import EnvData,replace_data
from common.handler_log import log
from common.handle_db import Handle_db
from decimal import Decimal

@ddt
class TestInvest(unittest.TestCase):
    excel=Handle_excel(os.path.join(DATA_DIR,'cases.xlsx'),'invest')
    cases=excel.read_data()
    db=Handle_db()

    @data(*cases)
    def test_invest(self,case):
        '''投资用例'''
        headers=eval(conf.get('env','headers'))
        # 如果不是登陆请求，则添加一个token
        if case['interface'] != 'login':
            headers['Authorization']=getattr(EnvData,'token')

        url=conf.get('env','BASE_URL')+case['url']
        method=case['method']
        # case['data']=replace_data(case['data'])
        # print(case['data'])
        data=eval(replace_data(case['data']))
        expected=eval(case['expected'])
        row=case['case_id']+1

        if case['check_sql']:
            sql1='select * from futureloan.invest where member_id= #member_id#;'
            start_invest_count=self.db.count(replace_data(sql1))

            sql2 = 'select leave_amount from futureloan.member where id= #member_id#;'
            start_leave_amount = self.db.find_one(replace_data(sql2))['leave_amount']

            sql3 = 'select * from futureloan.financelog where pay_member_id= #member_id#;'
            start_financelog_count = self.db.count(replace_data(sql3))

        response=request(method=method,json=data,url=url,headers=headers)
        res=response.json()

        # 如果是登陆接口，则提取用户Id+token
        if case['interface'] == 'login':
            member_id=str(jsonpath(res,'$..id')[0])
            token='Bearer '+jsonpath(res,'$..token')[0]
            setattr(EnvData,'member_id',member_id)
            setattr(EnvData,'token',token)

        # 如果是加标接口，则提取标Id
        if case['interface'] == 'add':
            loan_id=str(jsonpath(res,'$..id')[0])
            setattr(EnvData,'loan_id',loan_id)
            print(getattr(EnvData,'loan_id'))

        if case['check_sql']:
            sql1='select * from futureloan.invest where member_id= #member_id#;'
            end_invest_count=self.db.count(replace_data(sql1))

            sql2='select leave_amount from futureloan.member where id= #member_id#;'
            end_leave_amount = self.db.find_one(replace_data(sql2))['leave_amount']

            sql3='select * from futureloan.financelog where pay_member_id= #member_id#;'
            end_financelog_count=self.db.count(replace_data(sql3))




        try:
            self.assertEqual(res['code'],expected['code'])
            self.assertEqual(res['msg'],expected['msg'])
            # 判断是否需要进行sql校验
            if case['check_sql']:
                self.assertEquals(1,end_invest_count-start_invest_count)
                self.assertEquals(Decimal(str(data['amount'])),start_leave_amount-end_leave_amount)
                self.assertEquals(1, end_financelog_count - start_financelog_count)

                if case['title'] == '满标':

                    sql4 = 'select id from futureloan.invest where loan_id =#loan_id#;'
                    invest_ids = self.db.find_all(replace_data(sql4))
                    # setattr(EnvData,'invest_ids',invest_ids)

                    for invest_id in invest_ids:
                        sql5 = 'select * from futureloan.repayment where invest_id={}'.format(invest_id['id'])
                        count = self.db.count(sql5)
                        # 只要数据条数不为0即可校验通过
                        self.assertTrue(count)

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
