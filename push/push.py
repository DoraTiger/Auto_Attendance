#环境变量
from common.basicUtils import loadConfig
from common.basicUtils import getProxies

#日志服务
from common.basicLog import logger

#推送组件
from push.push_serverchan import push_serverchan
from push.push_email import get_email_config
from push.push_email import push_email
from push.push_discord import push_discord
class push_server():
    def __init__(self,debug=False):

        self.debug=debug
        # get proxy config
        self.proxise=getProxies()
        
        # get push config
        self.config=loadConfig("config.yaml","config")["push"]
        logger.debug('config:'+str(self.config))

        # get global config
        self.globalConfig=self.config["global"]
        logger.debug('global config:'+str(self.globalConfig))
        self.sendMsgOnlyError=self.globalConfig.get('sendMsgOnlyError',True)
        if(debug):
            self.sendMsgOnlyError=False

        # get channel config
        if(self.config.get('channel') is None):
            self.channelList={}
        else:
            self.channelList=self.config['channel']
        logger.debug('channelList:'+str(self.channelList))

    def set_personal_config(self,personal_config):
        if(self.debug):
            print(personal_config)
        for channel in personal_config:
            self.channelList.update({channel:personal_config[channel]})

    def pushMessage(self, message,title='推送服务测试标题',success=True):
        if success and self.sendMsgOnlyError==True:
            pass
        else:
            if(self.channelList.get('mail') and self.channelList["mail"].get('enable')==True):
                logger.debug(self.channelList["mail"])
                pushObj=push_email(get_email_config(self.channelList["mail"]))
                pushObj.pushMessage(message,title)
            if(self.channelList.get('serverChan') and self.channelList["serverChan"].get('enable')==True):
                logger.debug(self.channelList["serverChan"])
                pushObj=push_serverchan(self.channelList["serverChan"].get('sckey',''))
                pushObj.pushMessage(message,title)
            if(self.channelList.get('discord') and self.channelList["discord"].get('enable')==True):
                logger.debug(self.channelList["discord"])
                pushObj=push_discord(self.channelList["discord"].get('webhook',''))
                pushObj.set_proxies(self.proxise)
                pushObj.pushMessage(message,title)