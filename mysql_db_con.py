# -*- coding: utf-8 -*-
# @Time    : 2018/5/18 14:39
# @Author  : Zhang
# @FileName: mysql_db_con.py
# @Software: PyCharm
# @Blog    ：https://codedraw.cn
import pymysql


# connect mysql_db
db = pymysql.connect("localhost", "root", "0304", "student")


# close_db
def close_db(db, cursor):
    db.close()
    cursor.close()


# 初始化sql
def init_db():
    sql ="create table  `Student`(" \
            " `id` char(20),\
              `name` char(10),\
              `gender` char(2),\
              `phone` char(20),\
              `birthdate` char(20), \
              `address` char(40));"

    db.cursor().execute(sql)
    db.commit()


if __name__ == '__main__':
    init_db()
