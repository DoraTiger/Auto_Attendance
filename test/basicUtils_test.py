from fileinput import filename
import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from common.basicUtils import *

def test_loadConfig(filename='config.yaml'):
    print(loadConfig(filename))

if __name__ == '__main__':
    test_loadConfig()