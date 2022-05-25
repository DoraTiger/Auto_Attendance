from __future__ import annotations

import time

# import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger

# import projrct jobs
from job.daka import daka
from job.pterclub import pterclub
from job.hdatmos import hdatmos
from job.smzdm import smzdm
# import project utils
from common.basicLog import logger
from common.basicUtils import loadConfig

# import project push server
from push.push import push_server

def daka_job():
    logger.info("执行任务:"+daka.__name__)
    accountList = loadConfig('config.yaml', 'NEU_Health')['account']

    for account in accountList:
        _pushMsg = push_server()
        if(account.get('channel')):
            _pushMsg.set_personal_config(account['channel'])

        _jobObj = daka(account['studentID'], account['password'])
        msg, success = _jobObj.autoDaka()

        _pushMsg.pushMessage(msg, '健康打卡通知', success)


def pterclub_job():
    logger.info("执行任务:"+pterclub.__name__)
    accountList = loadConfig('config.yaml', 'pterclub')['account']

    for account in accountList:
        _pushMsg = push_server()
        if(account.get('channel')):
            _pushMsg.set_personal_config(account['channel'])

        _jobObj = pterclub()
        _jobObj.update_cookies(account['cookies'])
        msg, success = _jobObj.attendance()

        _pushMsg.pushMessage(msg, '猫站签到通知', success)

def hdatmos_job():
    logger.info("执行任务:"+hdatmos.__name__)
    accountList = loadConfig('config.yaml', 'hdatmos')['account']

    for account in accountList:
        _pushMsg = push_server()
        if(account.get('channel')):
            _pushMsg.set_personal_config(account['channel'])

        _jobObj = hdatmos()
        _jobObj.update_cookies(account['cookies'])
        msg, success = _jobObj.attendance()

        _pushMsg.pushMessage(msg, '阿童木签到通知', success)

def smzdm_job():
    logger.info("执行任务:"+smzdm.__name__)
    accountList = loadConfig('config.yaml', 'smzdm')['account']

    for account in accountList:
        _pushMsg = push_server()
        if(account.get('channel')):
            _pushMsg.set_personal_config(account['channel'])

        _jobObj = smzdm()
        _jobObj.update_cookies(account['cookies'])
        msg, success = _jobObj.attendance()
        
        _pushMsg.pushMessage(msg, '什么值得买签到通知', success)

def add_or_excute_job(scheduler, job_config, job_func, job_name=''):
    if(job_name == ''):
        job_name = job_func.__name__
    if(job_config['trigger']['enable']):
        logger.info(job_name+"计划启用,添加定时任务")
        trigger = CronTrigger.from_crontab(
            job_config['trigger']['cron'], timezone=job_config['trigger'].get('timezone', 'Asia/Shanghai'))
        scheduler.add_job(job_func, trigger, id=job_name, name=job_name)
    else:
        logger.info(job_name+"计划未启用,不添加定时任务，单次执行")
        job_func()


if __name__ == '__main__':
    scheduler = BackgroundScheduler(jobstores={'default': MemoryJobStore()}, executors={
                                    'default': ThreadPoolExecutor(20)})
    config = loadConfig('config.yaml')

    # add jobs
    if(config['NEU_Health']['enable']):
        add_or_excute_job(
            scheduler, config['NEU_Health'], daka_job, '东北大学健康打卡')
    if(config['pterclub']['enable']):
        add_or_excute_job(
            scheduler, config['pterclub'], pterclub_job, '猫站签到')
    if(config['hdatmos']['enable']):
        add_or_excute_job(
            scheduler, config['hdatmos'], hdatmos_job, '阿童木签到')
    if(config['smzdm']['enable']):
        add_or_excute_job(
            scheduler, config['smzdm'], smzdm_job, '什么值得买签到')

    # start scheduler
    if(scheduler.get_jobs()):
        logger.info("启动定时任务")
        scheduler.start()
        try:
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            logger.info("定时任务关闭成功")
