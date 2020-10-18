''' 
author:紫夏
Time:2020/9/26 21:09
'''
import pymysql
from common.handleConfig import conf

class Handle_db:

    def __init__(self):
        self.conn=pymysql.connect(host=conf.get('mysql','host'),
                             #      注意端口号是数值，用getint方法
                             port=conf.getint('mysql','port'),
                             user=conf.get('mysql','user'),
                             password=conf.get('mysql','password'),
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor
                             )
    #创建一个游标对象
        self.cursor=self.conn.cursor()

    def find_all(self,sql):
        self.conn.commit()
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def find_one(self,sql):
        self.conn.commit()
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def count(self,sql):
        '''返回数据条数'''
        self.conn.commit()
        res=self.cursor.execute(sql)
        return res

    def update(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        '''
        断开游标，关闭连接
        :return:
        '''
        self.cursor.close()
        self.conn.close()