import os
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/access')
def access():
    # response = requests.get('http://www.baidu.com')
    # if response.status_code == 200:
    #     return  {"code": 0, "msg": "ok", "data": "access success"}
    # else:
    #     return  {"code": 0, "msg": "ok", "data": "access failure"}
    return  {"code": 0, "msg": "ok", "data": "access success"}


if __name__ == '__main__':
    app.run(port=8080, debug=True)
