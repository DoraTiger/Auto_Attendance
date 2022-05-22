# Server酱发送依赖
from asyncio.log import logger
from urllib import response
import requests


class push_serverchan():
    def __init__(self, sckey):
        self.sckey = sckey

    def pushMessage(self, message, title='test title'):
        url = 'https://sctapi.ftqq.com/' + self.sckey + '.send'
        data = {
            'title': title,
            'desp': message
        }
        response = requests.post(url, data)
        if response.json().get('data').get('error') == 'SUCCESS':
            logger.debug("server酱 消息发送成功") 
        else:
            logger.debug("server酱 消息发送失败" + response.json().get('data'))
