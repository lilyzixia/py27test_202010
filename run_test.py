''' 
author:紫夏
Time:2020/8/30 12:20
'''

# import unittest
# from BeautifulReport import BeautifulReport
#
# suite=unittest.defaultTestLoader.discover(r'F:\python37test\02porttest20200829\day18')
# br=BeautifulReport(suite)
# br.report('demo2报告','report.html')


import unittest
from BeautifulReport import BeautifulReport
from common.handle_path import TESTCASE_DIR,REPORT_DIR
from common.handler_log import log
from common.send_email import send_msg
from HTMLTestRunnerNew import HTMLTestRunner

log.info('-------测试开始执行--------')

suite=unittest.TestSuite()
loader=unittest.TestLoader()
suite.addTest(loader.discover(TESTCASE_DIR))
# br=BeautifulReport(suite)
# br.report('测试接口',filename='portreport.html',report_dir=REPORT_DIR)


runner=HTMLTestRunner(stream=open('report.html','wb'),
                      title='27期测试报告',
                      tester='lisa',
                      description='第一个版本的测试')
runner.run(suite)




log.info('-------测试执行结束--------')

send_msg()