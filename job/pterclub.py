import requests
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))
from common.basicLog import logger


class pterclub():
    def __init__(self,debug=False) -> None:
        self.attendance_url='https://pterclub.com/attendance-ajax.php'

        self.my_session = requests.Session()
        self.my_session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Referer": "https://pterclub.com"
        })
        
        self.debug = debug

    def update_cookies(self,cookies):
        self.my_session.cookies.update(dict([line.strip().split('=', 1) for line in cookies.split("; ")]))

    def attendance(self):
        success = False
        msg=''

        response=self.my_session.get(self.attendance_url)
        if self.debug:
            print(response.text.encode('utf-8').decode('unicode_escape'))

        if response.json()['status'] == 1:
            success = True
            msg = response.json()['message']
        else:
            success = False
            msg = response.json()['message']

        return msg,success
