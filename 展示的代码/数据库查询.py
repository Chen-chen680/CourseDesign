import pymysql
import json
import re

class DataBaseTest():
    def __init__(self,):
        self.connect = pymysql.connect(
            host=''
            port=24817,
            user= ''
            password=''
            db=''
            charset='utf8mb4')
        self.cursor = self.connect.cursor()
        self.getSql()


    def getSql(self):

        out_data = []
        with open(r'泰山大众点评.txt', 'r', encoding='utf8') as f:
            content = f.readlines()
            for data in content:
                data = eval(data)
                user = data['name']
                time = data['date_time']
                star = data['star']
                comment = data['comment'].replace('收起评价','').encode('utf8')
                if len(comment) > 9999:
                    continue
                # comment = re.sub(r'\\x(..)','',comment)
                out_data.append((user, time, star, comment))
        self.out_data = out_data
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