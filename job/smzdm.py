
import json
import time
import requests
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from common.basicLog import logger

class smzdm():
    def __init__(self, debug=False) -> None:
        self.attendance_url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'

        self.my_session = requests.Session()
        self.my_session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Referer": "https://www.smzdm.com"
        })

        self.debug = debug

    def update_cookies(self, cookies):
        cookies=cookies.encode('utf-8').decode('unicode_escape')
        for line in cookies.split("; "):
            key, value = line.strip().split('=', 1)
            # if key == 'sensorsdata2015jssdkcross' or key == 's_his':
            #     continue
            self.my_session.cookies.set(key, value)

    def attendance(self):
        success = False
        msg=''

        attendance_form_items = {
            'callback': 'myCallback',
            '_': int(time.time() * 1000)
        }
        attendance_proxy_items = {
            'http': None,
            'https': None
        }
        attendance_response = self.my_session.get(
            self.attendance_url,
            params=attendance_form_items,
            proxies=attendance_proxy_items
        )

        # 去掉 callback 前缀
        tempStr=attendance_response.text.replace('callback(','').replace(')','') 
        # 去掉转义字符，转换中文编码
        tempStr=tempStr.replace('\\/','/').encode('utf-8').decode('unicode_escape') 
        # 去掉多余引号，适配json格式
        tempStr=tempStr.replace('<div class="signIn_data">','<div class=\\"signIn_data\\">').replace('<span class="red">','<span class=\\"red\\">')
        # 转换json格式
        tempJson=json.loads(tempStr)
        if self.debug:
            print(tempJson)

        if(tempJson['error_code']==0):
            msg= "签到成功，累计签到"+tempJson['data']['checkin_num']+"天"
            success = True
        else:
            msg=tempJson['error_msg']
            success = False
        return msg,success

