from __future__ import annotations


import time
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger

import job.daka as daka
from common.basicLog import logger
from common.basicUtils import loadConfig
from push.push import push_server



def daka_job():
    logger.info("执行定时打卡任务")
    studentList=loadConfig('config.yaml','student')
    _pushMsg=push_server()
    for student in studentList:
        _daka = daka.daka(student['studentID'], student['password'])
        msg,success=_daka.autoDaka()
        _pushMsg.pushMessage(msg,'健康打卡通知',success)



if __name__ == '__main__':
    triggerConfig=loadConfig('config.yaml','config')['trigger']
    if(triggerConfig.get('enable')):
        logger.info("打卡计划启用,开启自动打卡")
        scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()}, executors={'default': ThreadPoolExecutor(20)})
        scheduler.add_job(daka_job, CronTrigger.from_crontab(triggerConfig['cron']), id='daka_job', max_instances=1, misfire_grace_time=60)
        scheduler.start()
        logger.info("打卡计划启动成功")
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            logger.info("打卡计划关闭成功")
    else:
        logger.info("打卡计划未启用,单次调用任务")
        daka_job()

