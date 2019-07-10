# coding:utf8
import pymysql
from readconfig import ReadConfig


class MyMySQL:

    def __init__(self):
        self.conn = None
        self.cur = None
        self.data = ReadConfig()
        self.conn_mysql()

    def __enter__(self):
        return self

    def conn_mysql(self):
        '''连接数据库'''
        host = self.data.get_db("MySQL", "host")
        user = self.data.get_db("MySQL", "user")
        password = self.data.get_db("MySQL", "password")
        db = self.data.get_db("MySQL", "db")
        port = self.data.get_db("MySQL", "port")
        charset = self.data.get_db("MySQL", "charset")
        self.conn = pymysql.connect(host=host, user=user, password=password, port=int(port),db=db,charset=charset)
        self.cur = self.conn.cursor()

    def execute_sql(self, sql, data=None):
        self.conn_mysql()
        if data:
            self.cur.execute(sql, data)
        else:
            self.cur.execute(sql)
        self.conn.commit()

    def search(self, sql):
        self.conn_mysql()
        self.cur.execute(sql)
        return self.cur.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()
        print("mysql 正常退出")


if __name__ == "__main__":
    with MyMySQL() as c:
        sql = "show tables"
        result = c.search(sql)
        print(result)
