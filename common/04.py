''' 
author:紫夏
Time:2020/9/12 23:59
'''


import yaml
with open('conf.yaml',encoding='utf8') as f:
    file=yaml.load(f,Loader=yaml.FullLoader)
    print(file)
    print(file['log']['level'])
