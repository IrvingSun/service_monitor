#!coding=utf-8
import logging
import time
import os

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('monitor.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def Log(need_log, need_persist=False, data_file=None):
    """
    :param need_log: 是否需要显示日志
    :param need_persist: 是否需要持久化调用时间到文件
    :param data_file: 持久化文件的位置
    :return:
    """
    def performance_log(f):
        """在装饰器函数中返回新的函数"""
        def core(*args, **kw):
            st = time.time()
            fn = f(*args, **kw)
            et = time.time()
            if need_log:
                logger.info('调用一次完成,耗时：%0s秒' % (et - st))
            if need_persist:
                if not data_file:
                    pass
                try:
                    if not os.path.exists(data_file):
                        open(data_file,'w').close()

                    with open(data_file,'a') as data:
                        data.write('\n%s,%s' %(str(time.strftime('%Y-%m-%d %H:%M:%S')),int((et - st)*1000)))
                except Exception,e:
                    print e
                    pass

            return fn
        return core
    return performance_log
