import pymysql
import json
import re

class DataBaseTest():
    def __init__(self,):
        self.connect = pymysql.connect(
            host='sh-cynosdbmysql-grp-pwak5epk.sql.tencentcdb.com',
            port=24817,
            user='readonlyBigData',
            password='bigdatabig5',
            db='TestDataBase',
            charset='utf8mb4')
        self.cursor = self.connect.cursor()
        self.select()

    def select(self):
        try:
            result = self.cursor.execute('select * from CommentTable')
            data = self.cursor.fetchall()
            print(data)
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.connect.close()

if __name__ == '__main__':
    obj = DataBaseTest()