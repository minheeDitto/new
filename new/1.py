from twisted.python import log,logfile
from twisted.internet import reactor,task
import random
import time

DELAYTIME = 2

def fun():
    ret = random.random() * 2
    log.msg("本次执行的结果是%s"% ret)
    return ret

if __name__ == '__main__':
    log.startLogging(logfile.DailyLogFile("text.txt",'./'))
    log.msg("text task started at {}".format(time.asctime()))
    task1 = task.LoopingCall(fun)
    task1.start(DELAYTIME)
    reactor.run()

