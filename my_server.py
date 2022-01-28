# my_server.py
import os
import http.server # Our http server handler for http requests
import socketserver # Establish the TCP Socket connections
import json
import subprocess

PORT = 9000
my_subprocess = None    # 正在执行另一项独立任务

file_map = {
    'list_contacts': {
        'settings': './settings/list_contacts.yaml',
        'logs':     './logs/list_contacts.log',
        'cmd':      ['python', './src/wechat_helper.py', './tmp/list_contacts.yaml']
    },
    'list_saved_groups': {
        'settings': './settings/list_saved_groups.yaml',
        'logs':     './logs/list_saved_groups.log',
        'cmd':      ['python', './src/wechat_helper.py', './tmp/list_saved_groups.yaml']
    }
}

def get_settings_value(action):
    if action in file_map:
        filename = file_map[action]['settings']
        f = open(filename, 'r', encoding='utf-8')
        settings = f.read()
        f.close()
        return settings

    return None

# API请求：读取相应功能的settings
def api_settings_get(data):
    # print('api_settings_get...')
    settings = get_settings_value(data['action'])
    if settings != None:
        data['settings'] = settings
        return {
            'data': data,
            'state': 'ok',
            'msg': ''
        }
    else:
        return {
            'state': 'err',
            'msg': 'did not find settings'
        }
        print('!!! wrong action')

def get_logs_value(data):
    action = data['action']
    offset = 0
    if 'offset' in data:
        offset = data['offset']
    if action in file_map:
        filename = file_map[action]['logs']
        f = open(filename, 'r', encoding='utf-8')
        # print('set offset', filename, offset)
        f.seek(offset)
        logs = f.read()
        data['offset'] = f.tell()
        f.close()
        return logs

    return ''

def save_settings(filename, settings):
    file_dir = os.path.dirname(os.path.abspath(filename))
    os.makedirs(file_dir, exist_ok=True)

    f = open(filename, 'w', encoding='utf-8')
    f.write(settings)
    f.close()
    return filename

# API请求：执行所选择的功能
def api_run(data):
    global my_subprocess

    # 如果当前任务未完，新任务被忽略
    if my_subprocess != None:
        return api_logs_get(data)

    action = data['action']
    if action in file_map:
        cmd = file_map[action]['cmd']
        # 使用从用户UI获得的settings, 暂存临时文件
        settings_file = save_settings(cmd[2], data['settings'])
        print('subprocess:', cmd)
        my_subprocess = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        state = 'more'  # 通知前台持续更新log
    else:
        state = 'unkown action'
    return {
        'data': data,
        'state': state
    }

# API请求：读取相应功能的log输出结果
def api_logs_get(data):
    global my_subprocess

    data['log'] = get_logs_value(data)
    state = 'more'

    # 如果后台任务结束，通知前台不再更新log
    if my_subprocess != None:
        if my_subprocess.poll() != None:
            print('subprocess terminated.')
            # print(my_subprocess.stdout.read())
            state = 'ok'
            my_subprocess = None

    return {
        'data': data,
        'state': state
    }

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # print('get:', self.path)
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # print('post:', self.path)
        length = int(self.headers['Content-Length'])
        # print("HEADERS: ", self.headers)
        data = self.rfile.read(length).decode('utf-8')
        # print('<<', data, '>>')

        response_data = {}
        if self.path == '/api/settings/get':
            response_data = api_settings_get(json.loads(data))
        elif self.path == '/api/run':
            response_data = api_run(json.loads(data))
        elif self.path == '/api/logs/get':
            response_data = api_logs_get(json.loads(data))

        self.send_response(200)
        self.end_headers()

        self.wfile.write(bytes(json.dumps(response_data), 'utf-8'))
        return

Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Http Server Serving at port", PORT)
    httpd.serve_forever()
