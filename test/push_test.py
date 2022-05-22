import sys
from os.path import dirname, abspath
sys.path.append(dirname(dirname(abspath(__file__))))

from push.push import push_server
from push.push_serverchan import push_serverchan
from push.push_email import push_email


def test_push_server():
    pushObj=push_server()
    pushObj.pushMessage("test message","test title")

def test_push_serverchan():
    pushObj=push_serverchan("your own sckey")
    pushObj.pushMessage("test message","test title")

def test_push_email():
    pushObj=push_email(
        "testsender@test.test",
        "testreciever@test.test",
        "smtp.test.test",
        "testsender@test.test",
        "testtesttest",
        465)
    pushObj.pushMessage("test message","test title")

if __name__ == '__main__':
    # test_push_server()
    # test_push_serverchan()
    test_push_email()