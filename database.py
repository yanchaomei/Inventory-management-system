"""
此文件提供给GUI对数据库数据增删改查的接口。使用pymysql管理
使用者在自己主机跑的时候需要把第十二行中的第二个root改为自己mysql root用户的密码  以及 数据库创建过程在末尾，
不按步骤做跑不起来自己负责，自己去百度。我这里运行顺利。

"""

import pymysql
import datetime

class DataBase(object):
    def __init__(self, name):
        self.db = pymysql.connect("localhost", "root", "root", "药品库存管理系统")
        self.cursor = self.db.cursor()
        self.name = name
        # 获得table的字段名，在add函数中需要用到
        sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '{0}'".format(self.name)
        self.cursor.execute(sql)
        self.columns = self.cursor.fetchall()
        # 转换为标准格式
        temp = []
        for column in self.columns:
            temp.append(column[0])
        self.columns = tuple(temp)

    # 根据传入的数据，新建一条条目
    def Add(self, entry):
        sql = "INSERT INTO {0} ({1}) VALUES {2}".format(self.name,",".join(self.columns), entry)
        self.cursor.execute(sql)
        self.db.commit()

    # 删掉条目
    def Delete(self, index):
        sql = "DELETE FROM {0} WHERE id={1}".format(self.name, index)
        self.cursor.execute(sql)
        self.db.commit()

    # 修改某一条目
    def Change(self, index, field, entry):
        try:
            entry = int(entry)
            sql = "UPDATE {0} SET {1}={2} WHERE id={3}".format(self.name, field, entry, index)
        except:
            sql = "UPDATE {0} SET {1}='{2}' WHERE id={3}".format(self.name, field, entry, index)

        self.cursor.execute(sql)
        self.db.commit()

    # 查询出所有的条目，组成二维元组返回
    def Search(self, SQL=""):
        sql = "SELECT * FROM {0}".format(self.name)
        if SQL != "":
            self.cursor.execute(SQL)
        else:
            self.cursor.execute(sql)
        self.results = self.cursor.fetchall()
        return self.results

    def Close(self):
        self.db.close()


# 测试这个模块的API
if __name__ == '__main__':
    test = DataBase("盘点管理")
    results = test.Search()
    print(test.columns)
    test.Add((0,"待赋值", "待赋值",0, "待赋值", 0, "待赋值", 0, "待赋值", "待赋值", "待赋值"))

"""
create database 药品库存管理系统;

create table 库存基本数据(
id int primary key not null,
仓库大小 varchar(40) not null,
货架数量 int not null,
货架规格 varchar(20) not null,
推车数量 int not null,
推车规格 varchar(20) not null,
库工人数 int not null
);

create table 入库管理(
id int primary key not null,
产品代码 varchar(40) not null,
名称 varchar(40) not null,
入库数量 int not null,
单位 varchar(20) not null,
日期 varchar(20) not null,
操作者 varchar(20) not null,
存货货位 int not null
);

create table 出库管理(
id int primary key not null,
产品代码 varchar(40) not null,
名称 varchar(40) not null,
出库数量 int not null,
单位货 varchar(20) not null,
日期 varchar(20) not null,
操作者 varchar(20) not null,
出存单位 int not null
);

create table 盘点管理(
id int primary key not null,
产品代码 varchar(40) not null,
名称 varchar(40) not null,
出库数量 int not null,
出库单位 varchar(20) not null,
入库数量 int not null,
入库单位 varchar(20) not null,
结余 int not null,
空余货位 varchar(20),
日期 varchar(20) not null,
操作者 varchar(20) not null
);
"""