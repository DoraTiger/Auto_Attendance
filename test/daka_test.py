import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from common.basicUtils import loadConfig
from common.basicLog import logger

from job.daka import daka

def test_health_daka():
    logger.debug("执行健康打卡测试")
    accountList=loadConfig('config.yaml','NEU_Health')['account']
    for account in accountList:
        _daka = daka(account['studentID'], account['password'])
        _daka.login()
        msg,success=_daka.healthDaka()
        logger.debug(msg)
        break

def test_temperature_daka():
    logger.debug("执行体温打卡测试")
    accountList=loadConfig('config.yaml','student')['account']
    for account in accountList:
        _daka = daka(account['studentID'], account['password'])
        _daka.login()
        msg,success=_daka.temperatureDaka()
        logger.debug(msg)
        break

if __name__ == '__main__':
    # test_health_daka()
    test_temperature_daka()
