#!encoding=UTF-8
import random
import time

import params
from util import log, httpUtil, dateUtil, mailUtil, analyzeUtil
from util.log import logger

# webservice url
WS_URL = params.ws_url
# 取样次数（请求重复次数）
SAMPLING_COUNT = params.sampling_count
# 监控间隔时间 秒
INTERVAL = params.interval
DATA_PATH = params.data_txt_location
DATA_TXT_SEPARATOR = params.data_txt_separator
SUCCESS_FLAG = params.success_flag
MAX_FAIL = params.max_fail
TO_LIST = params.to_list
USE_CRONTAB = params.use_crontab
# 主题
SUB = 'BaseWS Dubbo服务异常'
# 文件正文内容
CONTENT = '''
<HTML><HEAD></HEAD>
<BODY>
<H3>Hi, all:</H3>
<p style="text-indent: 2em">
您好，BaseWS Dubbo服务监控，调用失败 <font color="red"><b>%(failTimes)d</b></font> 次，超过报警阀值 <b>%(times)d</b>
<div>当前时间：%(currentTime)s</div>
<div>调用时间：<br/>%(analyzeLog)s</div>
<br/>
邮件为自动发送，请勿回复。
</p>
</BODY></HTML>
'''


class Monitor:

    def __init__(self):
        pass

    def http_check(self, type='POST', media_type='application/json', data=None, header={}, timeout=1000):
        logger.info("-------BaseWS Dubbo服务监控-------")

        success = 0
        fail = 0
        result_flag = False
        time_cost = []
        times = 0
        for i in xrange(SAMPLING_COUNT):

            #GET请求，直接发送过去
            if type == 'GET':
                http_result = httpUtil.do_get(url=WS_URL,timeout=timeout)
                result_parser = lambda x: x.find(SUCCESS_FLAG) >= 0
                result_flag = result_parser(http_result[0])
                time_cost.append(http_result[1])
                # logger.info('result=%s, result_flag=%s ,time=%s' % (http_result[0], result_flag, http_result[1]))
            times += 1
            if result_flag:
                success += 1
            else:
                fail += 1

        if not result_flag:
            analyzeLog = analyzeUtil.analyze(time_cost, success, fail)

        if fail > MAX_FAIL:
            analyzeLog = analyzeUtil.analyze2html(time_cost, success, fail)
            msg = CONTENT % {'failTimes': fail, 'times': MAX_FAIL, 'currentTime': dateUtil.getCurrentTime(), 'analyzeLog': analyzeLog}
            logger.info('send_email,message=' + msg)
            mailUtil.send_email(msg, SUB, TO_LIST)

if __name__ == '__main__':
    monitor = Monitor()
    # 使用linux定时任务crontab
    if USE_CRONTAB:
        monitor.http_check(type='GET')
    else:
        while True:
            monitor.http_check(type='GET')
            time.sleep(INTERVAL)
