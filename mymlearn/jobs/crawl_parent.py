# coding:utf8
from decimal import Decimal
from utils.mymysql import MyMySQL


class DbItem:
    def __init__(self):
        pass

    def insert(self,table):
        fields = ""
        values = ""
        for k, v in self.__dict__.items():
            if v!= None:
                fields += k +","
                if not isinstance(v,int) and not isinstance(v,Decimal):
                   values += '"'+ str(v) + '",'
                else:
                    values += str(v)+","
        fields, values = fields[:-1], values[:-1]
        sql = "insert into {0}({1}) values({2})".format(table, fields, values)
        print(sql)
        with MyMySQL() as m:
            m.execute_sql(sql)


class CrawlParent:

    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"

    def __init__(self):
        pass
