''' 
author:紫夏
Time:2020/10/11 13:26
'''

import re
from common.handleConfig import conf

class EnvData:
    '''定义一个类，用来保存用例执行过程中，提取出来的数据'''
    pass


def replace_data(data):
    '''替换数据'''
    while re.search('#(.*?)#',data):
        res=re.search('#(.*?)#',data)

        key=res.group()
        item=res.group(1)
        try:
            # 获取配置文件中的对应值
            value=conf.get('test_data',item)
        except:
            # 去EnvData找 （环境变量）
            value=getattr(EnvData,item)
        data=data.replace(key,value)
    return data


