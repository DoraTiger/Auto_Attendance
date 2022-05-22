# 邮件发送依赖
from email.mime.text import MIMEText
from email.header import Header
import smtplib

# 日志服务
from common.basicLog import logger


def get_email_config(config):
    sender = config.get('sender', '')
    receiver = config.get('receiver', '')
    mailHost = config.get('host', '')
    mailUser = config.get('sender', '')
    mailPass = config.get('password', '')
    mailPort = config.get('port', 465)
    return sender, receiver, mailHost, mailUser, mailPass, mailPort


class push_email():

    def __init__(self, sender, receiver, mailHost, mailUser, mailPass, mailPort) -> None:
        self.sender = sender
        self.receiver = receiver
        self.mailHost = mailHost
        self.mailUser = mailUser
        self.mailPass = mailPass
        self.mailPort = mailPort

    def pushMessage(self, message, title='测试邮件'):
        # 邮件普通文本内容
        mailContent = message
        message = MIMEText(mailContent, 'plain', 'utf-8')
        # 发送人名称
        message['From'] = Header(title, 'utf-8')
        # 收件人名称
        message['To'] = Header(self.receiver, 'utf-8')
        # 邮件标题
        message['Subject'] = Header(title, 'utf-8')

        try:
            smtpObj = smtplib.SMTP_SSL(self.mailHost, self.mailPort)
            smtpObj.login(self.mailUser, self.mailPass)
            logger.debug(self.receiver+" 邮件发送成功")
        except smtplib.SMTPException:
            logger.error('Error: 无法发送邮件')
