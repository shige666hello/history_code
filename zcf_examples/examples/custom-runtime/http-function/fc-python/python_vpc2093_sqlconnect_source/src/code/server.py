import os
from flask import Flask, render_template
import os
import requests
import json
import pymysql

app = Flask(__name__)

@app.route('/access')
def access():
    response = requests.get('http://www.baidu.com')
    if response.status_code == 200:
        return  {"code": 0, "msg": "ok", "data": "access success"}
    else:
        return  {"code": 0, "msg": "ok", "data": "access failure"}


@app.route('/')
def hello_world():
    print("http connect success,next sql conn…")
    # connect = pymysql.Connect(     # 连接数据库
    #     host='11.121.83.171',
    #     port=22263,
    #     user='super16451_rw',
    #     passwd='61f6e0a716e77634',
    #     db='testzcffunc',
    #     charset='utf8'
    # )
    connect = pymysql.Connect(     # 连接数据库
        host='11.121.97.121',
        port= 22052,
        user='super16432_rw',
        passwd='617b1f4d53afd3a7',
        db='zcftest',
        charset='utf8'
    )
    # 3、执行SQL语句
    cursor = connect.cursor()  # 获取游标
    sql = "show databases;"  # 获取所有数据库
    cursor.execute(sql)
    print(cursor.fetchall())
    print("sql connnect success!!!")

    # 4、关闭数据库
    cursor.close()
    connect.close()
    return  {"code": 0, "msg": "ok", "data": "hello world"}

if __name__ == '__main__':
    app.run(port=8080, debug=True)
