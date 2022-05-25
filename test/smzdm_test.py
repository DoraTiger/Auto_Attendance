import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from common.basicUtils import loadConfig
from common.basicLog import logger

from job.smzdm import smzdm

def test_smzdm():
    logger.debug("执行什么值得买签到测试")
    accountList=loadConfig('config.yaml','smzdm')['account']
    for account in accountList:
        _test=smzdm(True)
        _test.update_cookies(account.get('cookies'))
        msg,success=_test.attendance()
        print(success,msg)
        logger.debug(msg)
        break

if __name__ == '__main__':
    # test_health_daka()
    test_smzdm()
