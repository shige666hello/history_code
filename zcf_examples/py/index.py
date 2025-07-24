# server.py
import sys
import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class FunctionHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 读取请求（事件数据）
        content_length = int(self.headers['Content-Length'])
        event = json.loads(self.rfile.read(content_length))

        # 调用函数逻辑（假设函数在function.py中）
        from function import handler
        result = handler(event, {})  # 调用用户定义的handler

        # 返回结果
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())


if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 9000), FunctionHandler)
    server.serve_forever()