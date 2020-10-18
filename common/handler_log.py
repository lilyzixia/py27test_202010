''' 
author:紫夏
Time:2020/9/5 13:23
'''

import logging
from common.handleConfig import conf
import os
from common.handle_path import LOG_DIR

log_filepath=os.path.join(LOG_DIR,conf.get('log','filename'))

class HandleLogger:
    @staticmethod
    def create_logger():
        mylog = logging.getLogger("zixia")
        mylog.setLevel(conf.get('log','level'))

        fh = logging.FileHandler(log_filepath, encoding="utf8")
        fh.setLevel(conf.get('log','fh_level'))
        mylog.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel(conf.get('log','sh_level'))
        mylog.addHandler(sh)

        formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        # format = logging.Formatter(conf.get('log','formats'))
        format = logging.Formatter(formats)
        sh.setFormatter(format)
        fh.setFormatter(format)

        return mylog

log=HandleLogger.create_logger()