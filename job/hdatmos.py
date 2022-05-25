from socket import MsgFlag
import requests

from common.basicLog import logger


class hdatmos():
    def __init__(self,debug=False) -> None:
        self.attendance_url='https://hdatmos.club/attendance.php'

        self.my_session = requests.Session()
        self.my_session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Referer": "https://hdatmos.club"
        })
        
        self.debug = debug

    def update_cookies(self,cookies):
        self.my_session.cookies.update(dict([line.strip().split('=', 1) for line in cookies.split("; ")]))

    def attendance(self):
        success = False
        msg=''

        response=self.my_session.get(self.attendance_url)
        if self.debug:
            print(response.text)
        if(response.text.find('签到成功')!=-1):
            msg=response.text[response.text.find('<td class="text" >')+19:response.text.find('<span style="float:right">今日签到排名：<b>')].replace('</b>','').replace('<b>','').replace('<p>','').split('。')[0]
            success = True
        else:
            msg='签到失败，请手动完成签到'
            success = False
        logger.info(msg)
        return success,msg



if __name__ == '__main__':
    cookietext=""
    _test=hdatmos()
    _test.update_cookies(cookietext)
    success,msg=_test.attendance()
    print(msg)
