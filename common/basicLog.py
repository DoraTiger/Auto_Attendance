import logging
from enum import Enum
from common.basicUtils import loadConfig

# config = loadConfig("config.yaml", "config")
# print(config['log'].get('level', 'INFO'))
# print(logLevel("DEBUG"))
# logging.basicConfig(
#     level=config['log'].get('level', 'INFO'),
#     datefmt='%Y-%m-%d %H:%M:%S',
#     format='%(asctime)s %(filename)s %(levelname)s %(message)s',
#     filename=config['log'].get('file', 'daka.log'))

# logger=logging.getLogger(__name__)

def getLoggerLevel():
    config = loadConfig("config.yaml", "config")
    log_level=config['log'].get('level', 'INFO')
    level_range=['DEBUG','INFO','WARNING','ERROR','CRITICAL']
    if log_level.upper() not in level_range:
        log_level='INFO'
    
    if(log_level.upper()=='DEBUG'):
        return logging.DEBUG
    if(log_level.upper()=='INFO'):
        return logging.INFO
    if(log_level.upper()=='WARNING'):
        return logging.WARNING
    if(log_level.upper()=='ERROR'):
        return logging.ERROR
    if(log_level.upper()=='CRITICAL'):
        return logging.CRITICAL

def getLoggerFile():
    config = loadConfig("config.yaml", "config")
    log_file=config['log'].get('file', 'daka.log')
    
    return log_file

logging.basicConfig(
    level=getLoggerLevel(),
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
    filename=getLoggerFile(),
    filemode='a')
logging.FileHandler.encoding='utf-8'
logger=logging.getLogger(__name__)


if __name__ == '__main__':
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")
    
