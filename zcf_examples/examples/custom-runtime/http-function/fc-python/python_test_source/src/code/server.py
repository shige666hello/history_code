import os
from flask import Flask, render_template
import requests
import json
import pymysql

app = Flask(__name__)

@app.route('/sql')
def test_sql():

    connect = pymysql.Connect(     # 连接数据库
        host='11.121.83.171',
        port=22263,
        user='super16451_rw',
        passwd='61f6e0a716e77634',
        db='testzcffunc',
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

@app.route('/add')
def test_env():
    # print("set env")
    # os.environ['a'] = "1"
    # os.environ['b'] = "2"
    print("get env")
    print(os.environ)
    print("http connect success,next sql conn…")

    # 3、使用环境变量做加法，默认环境变量有a、b
    k1 = os.environ['a']
    k2 = os.environ['b']
    c = int(k1)+int(k2)
    print("a+b=", c)
    return  {"code": 0, "msg": "ok", "data": f"a+b={c}"}

@app.route('/')
def hello_world():
    return {"code": 0, "msg": "ok", "data": "hello world"}
if __name__ == '__main__':
    app.run(port=8080, debug=True)
