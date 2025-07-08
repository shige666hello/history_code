import http.server
import socketserver
import os
import requests
import json
import pymysql
PORT = 8080

web_dir = os.path.join(os.path.dirname(__file__), 'web')
os.chdir(web_dir)

class SimpleHTTPRequestHandlerWithRouting(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/hello':

            self.do_CUSTOM_ROUTE()
        else:
            return super().do_GET()

    def access(self):
        response = requests.get('http://www.baidu.com')
        if response.status_code == 200:
            self.send_response(response.status_code)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'access success')
        else:
            self.send_response(response.status_code)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'access failure')

    def do_CUSTOM_ROUTE(self):
        # response = requests.get('https://api.github.com/users/octocat')
        # if response.status_code == 200:
        print("http connect success,next sql conn…")

        # connect = pymysql.Connect(     # 连接数据库
        #     host='11.121.97.121',
        #     port=22052,
        #     user='super16432_rw',
        #     passwd='617b1f4d53afd3a7',
        #     db='zcftest',
        #     charset='utf8'
        # )
        connect = pymysql.Connect(     # 连接数据库
            host='11.40.82.184',
            port=22111,
            user='super16451_rw',
            passwd='4f99d49e46c80bf1',
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
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'This is a custom route response.')
        # self.wfile.write({'statusCode': 200, 'body': 'Success!'})
        # self.wfile.write(json.dumps(response.json()).encode('utf-8'))
        # else:
        #     self.send_response(response.status_code)
        #     self.send_header('Content-type', 'text/plain')
        #     self.end_headers()
        #     self.wfile.write(b'Error.')
            # self.wfile.write({'statusCode': response.status_code, 'body': 'Error'})


def run(server_class=http.server.HTTPServer, handler_class=SimpleHTTPRequestHandlerWithRouting):
    print("aaaaaaa")
    server_address = ('', PORT)  # 服务器监听在0.0.0.0的8000端口
    httpd = server_class(server_address, handler_class)
    print('HTTP server running on port 8080')
    httpd.serve_forever()


run()