#!encoding=UTF-8

from log import logger


def analyze(time_cost, success_count, fail_coun):
    total_cost = reduce((lambda x, y: x + y), time_cost)
    analyzeLog = '本次测试完成，耗时: %0s秒，成功：%0s，失败：%0s \n' % (
        total_cost, success_count, fail_coun)
    analyzeLog += ('%0s%20s%20s \n' % ('Avg', 'Max', 'Min'))
    analyzeLog += ('%0s%20s%20s \n' %
                   (total_cost / len(time_cost), max(time_cost), min(time_cost)))
    analyzeLog += '#' * 40
    logger.info(analyzeLog)
    return analyzeLog


def analyze2html(time_cost, success_count, fail_coun):
    total_cost = reduce((lambda x, y: x + y), time_cost)
    analyzeLog = '<span>' + ('本次测试完成，耗时: %0s秒，成功：%0s，失败：%0s \n' %
                             (total_cost, success_count, fail_coun)) + '</span>'
    analyzeLog += '<table border="1">'
    analyzeLog += '<thead> <tr> <td>Avg</td> <td>Max</td> <td>Min</td> </tr> </thead>'
    analyzeLog += '<tbody> <tr> <td>%0s</td> <td>%0s</td> <td>%0s</td> </tr> </tbody>' % (
        total_cost / len(time_cost), max(time_cost), min(time_cost))
    analyzeLog += '</table>'
    analyzeLog += '<span>' + ('#' * 40) + '</span>'
    return analyzeLog
