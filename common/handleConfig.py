''' 
author:紫夏
Time:2020/9/11 0:19
'''


from configparser import ConfigParser
from common.handle_path import CONF_DIR
import os

class HandleConfig(ConfigParser):
    '''重写init方法'''
    def __init__(self,filename):
        super().__init__()
        self.read(filename,encoding='utf8')

conf=HandleConfig(os.path.join(CONF_DIR,'conf.ini'))
