# coding:utf8
import configparser
import os


class ReadConfig:
    '''定义了一个读取配置文件的类'''

    def __init__(self,filepath = None):
        if filepath:
            configpath = filepath
        else:
            root_dir = os.path.dirname(__file__)
            configpath = os.path.join(root_dir, "config.ini")
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def get_db(self, sec, param):
        return self.cf.get(sec, param)


if __name__ == "__main__":
    t = ReadConfig()
    print(t.get_db("MySQL-Offline", "host"))
