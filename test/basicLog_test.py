import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from common.basicLog import logger

if __name__ == '__main__':
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")