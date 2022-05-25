import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from common.basicUtils import loadConfig
from common.basicLog import logger

from job.hdatmos import hdatmos

def test_hdatmos():
    logger.debug("执行阿童木签到测试")
    accountList=loadConfig('config.yaml','hdatmos')['account']
    for account in accountList:
        _test=hdatmos(True)
        _test.update_cookies(account.get('cookies'))
        msg,success=_test.attendance()
        print(success,msg)
        logger.debug(msg)
        break

if __name__ == '__main__':
    # test_health_daka()
    test_hdatmos()
