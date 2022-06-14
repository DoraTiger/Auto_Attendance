import re
import time
import requests

from common.basicLog import logger

class daka():
    def __init__(self, studentID, password,debug=False):
        self.studentID = studentID
        self.password = password
        self.debug = debug

        self.token = ''
        self.name = ''
        self.lt = ''
        self.my_session = requests.Session()

        self.login_url = 'https://e-report.neu.edu.cn/login'
        self.post_url = 'https://pass.neu.edu.cn/tpass/login'
        self.create_url = 'https://e-report.neu.edu.cn/notes/create'
        self.note_url = 'https://e-report.neu.edu.cn/api/notes'
        self.item_url = 'https://e-report.neu.edu.cn/inspection/items'

    def login(self):
        # 登陆，更新session
        msg = ''
        success = False
        try:
            login_response = self.my_session.get(self.login_url)
            self.lt = re.findall(
                r'LT-[0-9]*-[0-9a-zA-Z]*-tpass', login_response.text, re.S)[0]

            login_form_items = {
                'rsa': self.studentID + self.password + self.lt,
                'ul': str(len(self.studentID)),
                'pl': str(len(self.password)),
                'lt': self.lt,
                'execution': 'e1s1',
                '_eventId': 'submit'
            }
            
            post_response = self.my_session.post(self.post_url, login_form_items)
            logger.debug(post_response.status_code)

            if post_response.status_code == 200:
                # 更新token,name
                note_response = self.my_session.get(self.create_url)
                self.token = re.findall(
                    r'name=\"_token\"\s+value=\"([0-9a-zA-Z]+)\"', note_response.text, re.S)[0]
                self.name = re.findall(r'当前用户：\s*(\w+)\s*',
                                    note_response.text, re.S)[0]

                msg = self.studentID+'登录成功!'
                success = True
            else:
                msg = self.studentID+'登录失败！请手动完成打卡'
                success = False
        except(Exception) as e:
            logger.error(e)
            msg = self.studentID+'登录失败!请手动完成打卡!'
            success = False
        logger.info(msg)
        return msg, success

    def healthDaka(self):
        # 健康打卡
        msg = ''
        success = False
        try:
            health_items = {
                '_token': self.token,
                'jibenxinxi_shifoubenrenshangbao': '1',
                'profile[xuegonghao]': self.studentID,
                'profile[xingming]': self.name,
                'profile[suoshubanji]': '',
                'jiankangxinxi_muqianshentizhuangkuang': '正常',
                'xingchengxinxi_weizhishifouyoubianhua': '0',
                'cross_city': '无',
                'qitashixiang_qitaxuyaoshuomingdeshixiang': ''
            }

            health_response = self.my_session.post(self.note_url, health_items)
            logger.debug(health_response.status_code)

            if health_response.status_code == 201:
                msg = self.studentID+'健康打卡成功!'
                success = True
            else:
                msg = self.studentID+'健康打卡失败！请手动完成打卡！'+ str(health_response.status_code)
                success =  False
        except(Exception) as e:
            logger.error(e)
            msg = self.studentID+'健康打卡失败！请手动完成打卡！'+ '异常退出'
            success =  False
        logger.info(msg)
        return msg, success

    # 通过移动端接口，查询是否打卡
    # 打卡成功获取结果为<img class="successImg" src="https://e-report.neu.edu.cn/mobile/success.png">
    # 未打卡获取结果为<p class="healthNone">待填报</p>
    def checkHealthDaka(self):
        item_response = self.my_session.get(self.item_url)
        checkMsg = re.findall(
            r'\<a\s+href=\"https://e-report.neu.edu.cn/mobile/notes/create\"\s+\>(.+)\<div\s+class=\"calendaDiv\"\s+\>', item_response.text, re.S)[0]
        if re.match(r'.+class=\"successImg\".+', checkMsg, re.S):
            return True
        else:
            return False

    def temperatureDaka(self):
        # 体温打卡
        msg = ''
        success = False
        try:
            hour = (time.localtime().tm_hour) % 24
            temperature_url = 'https://e-report.neu.edu.cn/inspection/items/{}/records'.format(
                ('1' if 7 <= hour <= 9 else '2' if 12 <= hour <= 14 else '3'))
            temperature_items = {
                '_token': self.token,
                'temperature': '36.5',
                'suspicious_respiratory_symptoms': '0',
                'symptom_descriptions': ''
            }
            temperature_response = self.my_session.post(temperature_url,temperature_items)
            logger.debug(temperature_response.status_code)

            if temperature_response.status_code == 200:
                msg = self.studentID+'体温打卡成功!'
                success = True
            else:
                msg = self.studentID+'体温打卡失败！请手动完成打卡！'
                success = False
        except(Exception) as e:
            logger.error(e)
            msg = self.studentID+'体温打卡失败！请手动完成打卡！'
            success=False
        logger.info(msg)
        return msg, success

    # 判断是否是体温打卡时间段(07:00~09:00,12:00~14:00,19:00~21:00)
    def checkTimeTemperatureDaka(self):
        timeNow = time.strftime('%H', time.localtime())
        if re.match(r'^(07|08|12|13|19|20)', timeNow, re.S):
            return True
        else:
            return False

    def autoDaka(self):
        # 自动打卡
        pushMsg = ''
        loginMsg, loginSuc = 'skip', False
        healthMsg, healthSuc = 'skip', False
        temperatureMsg, temperatureSuc = 'skip', False
        
        loginMsg, loginSuc =self.login()
        
        if loginSuc:
            if self.checkHealthDaka():
                healthMsg, healSuc = self.studentID+'健康已打卡,不重复打卡!', True
            else:
                healthMsg, healSuc = self.healthDaka()

            if self.checkTimeTemperatureDaka():
                temperatureMsg, tempSuc = self.temperatureDaka()
            else:
                temperatureMsg, tempSuc = self.studentID + \
                    '不是体温打卡时间段，不打卡!', False

        pushMsg = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + \
            '\n'+loginMsg+'\n'+healthMsg+'\n'+temperatureMsg
        logger.info(pushMsg)

        return pushMsg, loginSuc and healSuc and tempSuc
