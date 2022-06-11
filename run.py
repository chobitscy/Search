import logging
import os
import platform
import sys
import time

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


def fd(keyword):
    response = os.popen(
        r'lib\%s -p %s %s' % ('fd.exe' if platform.system() == 'Windows' else 'fd', keyword, workspace))
    result = response.buffer.read().decode('utf-8')
    response.close()
    file_list = []
    for x in result.split('\n'):
        if x == '' or os.path.isdir(x):
            continue
        info = os.stat(x)
        file_name = os.path.basename(x)
        size = int(info.st_size)
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(info.st_ctime))
        file_list.append({
            'resource': x,
            'file': file_name,
            'size': size,
            'date': create_time,
            'type': 'local'
        })
    return file_list


@app.route("/search/<keyword>")
def run(keyword: str):
    data = fd(keyword)
    return jsonify(data)


if __name__ == '__main__':
    try:
        args = sys.argv
        if len(args) < 2:
            raise ValueError('缺少工作空间参数')
        workspace = args[1]
        print(workspace)
        app.run()
    except Exception as e:
        logging.exception(e)
