# -*- coding: utf-8 -*-

import time
import datetime

defaultTimeFomartStr = "%Y-%m-%d %H:%M:%S"


def getYesterday():
    # 时间
    today = datetime.datetime.now()
    return (today + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')


def getToday():
    # 时间
    today = datetime.datetime.now()
    return today.strftime('%Y-%m-%d')


def getHour():
    # 时间
    today = datetime.datetime.now()
    return today.strftime('%H')


def getCurrentTime():
    # 时间
    today = datetime.datetime.now()
    return today.strftime(defaultTimeFomartStr)


def getTimeStamp(timeStr, timeFomart=defaultTimeFomartStr):
    # 时间
    timeArray = time.strptime(timeStr, timeFomart)
    return toTimeStamp(timeArray)


def getCurrentTimeStamp():
    # 时间
    timeArray = time.localtime()
    return toTimeStamp(timeArray)


def toTimeStamp(timeArray):
    # 转换为时间戳: 秒为单位
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def hoursdiff(d1, d2):
    return (d1 - d2) / 3600

if __name__ == '__main__':
    print getCurrentTime()
    print time.localtime()
    print getCurrentTimeStamp()
