''' 
author:紫夏
Time:2020/9/26 17:58
'''

import os

# 获取当前文件的父级路径的父级路径=主目录
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TESTCASE_DIR=os.path.join(BASE_DIR,'testcases')
DATA_DIR=os.path.join(BASE_DIR,'data')
CONF_DIR=os.path.join(BASE_DIR,'conf')
REPORT_DIR=os.path.join(BASE_DIR,'report')
LOG_DIR=os.path.join(BASE_DIR,'logs')
