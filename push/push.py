#环境变量
from common.basicUtils import loadConfig

#日志服务
from common.basicLog import logger

#推送组件
from push.push_serverchan import push_serverchan
from push.push_email import get_email_config
from push.push_email import push_email

class push_server():
    def __init__(self,debug=False):
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
        self.channelList=self.config['channel']
        logger.debug('channelList:'+str(self.channelList))

    def pushMessage(self, message,title='推送服务测试标题',success=True):
        if success and self.sendMsgOnlyError==True:
            pass
        else:
            if(self.channelList["mail"].get('enable')==True):
                logger.debug(self.channelList["mail"])
                pushObj=push_email(get_email_config(self.channelList["mail"]))
                pushObj.pushMessage(message,title)
            if(self.channelList["serverChan"].get('enable')==True):
                logger.debug(self.channelList["serverChan"])
                pushObj=push_serverchan(self.channelList["serverChan"].get('sckey',''))
                pushObj.pushMessage(message,title)