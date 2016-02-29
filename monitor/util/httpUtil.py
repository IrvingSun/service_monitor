#!encoding=UTF-8
import urllib
import urllib2
import time
import params
try:
    import json
except ImportError:
    import simplejson as json
import traceback
from log import logger, Log


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:37.0) Gecko/20100101 Firefox/37.0'


def http_post(media_type='application/json', url='', data=None, timeout=100, header={}):
    if not header:
        header['Content-Type'] = media_type
        header['User-Agent'] = user_agent

    multi_result = do_post(url, data, header, timeout)
    return multi_result


def http_get(url='', data=None, timeout=100):
    """ data 字典类型 """
    if data is not None:
        if '?' not in url:
            url += '?'
        url += '&' + urllib.urlencode(data)
    url += "&_=" + str(time.time())
    # logger.info(url)
    multi_result = do_get(url, timeout)
    return multi_result


@Log(True,True,params.post_persist_location)
def do_get(url, timeout=100):
    # print url,data
    st = time.time()
    req = urllib2.Request(url)
    response = ''
    try:
        res_data = urllib2.urlopen(req)
        response = res_data.read()
    except Exception, e:
        logger.error('http do_get error')
        # logger.error(traceback.format_exc())
        pass
    et = time.time()
    # logger.info('response='+response)
    return [response, et - st]


@Log(True,True,params.post_persist_location)
def do_post(url, data=None, header={}, timeout=100):
    # print url,data
    st = time.time()
    if not data:
        return False
    req = urllib2.Request(url, headers=header)
    req.add_data(data)
    response = ''
    try:
        res_data = urllib2.urlopen(req)
        response = res_data.read()
    except Exception, e:
        logger.error('http do_post error')
        # logger.error(traceback.format_exc())
        pass
    et = time.time()
    # logger.info('response='+response)
    return [response, et - st]
