#!coding=utf-8
import os
import linecache
import sys, getopt

"""
获取一定数目(默认100条 )数据进行如下几个方面的分析:
时间段
最长用时，最短用时，平均用时，超过平均值的次数，低于平均值的次数
在各个时间段的分布次数和比例
"""

header_format = '%-*s%*s%*s'

BASE_CONTENT =  '分析的时间段为：%s ~ %s,'\
                '总共有%d次请求\n'\
                '最长用时:%d ms,最短用时:%d ms,平均用时:%d ms\n'\
                '超过平均用时:%d次,低于平均用时:%d次'

ADVANCE_CONTENT_HEAD =  header_format % (25,'用时(ms)',10, '次数',17,'比例')

STEP = 10

def read_data(file, nums=100):
    """
    :param file: 耗时文件位置
    :param nums: 最多读取的条数
    :return:
    """
    result = []
    if os.path.exists(file):
        count = len(linecache.getlines(file))
        if nums >= count:
            return map(lambda x : x.strip('\n').split(','), linecache.getlines(file))
        else:
            start = count - nums + 1
            while start <= count:
                result.append(linecache.getline(file, start).strip('\n').split(','))
                start+=1
    return result


def split_data(datas):
    current_time = []
    cost_time = []
    map(lambda x : len(x)==2 and (current_time.append(x[0]) or cost_time.append(int(x[1]))) ,datas)

    return current_time, cost_time,datas

def statistics_data(items,average):
    below,over =0,0
    for x in items:
        if x >= average:
            over += 1
        else:
            below += 1
    return below,over

def print_advance(section):
    if len(section['times']) == 0:
        return
    print header_format % (20,section['start']+' ~ '+section['end'],10, str(len(section['times'])),15,
                           (section['rate']))

def usage():
    print "帮助信息:\n获取一定数目(默认100条 )数据进行如下几个方面的分析:\n\
            时间段,最长用时，最短用时，平均用时，超过平均值的次数，低于平均值的次数,\n\
            在各个时间段的分布次数和比例\n \
            -h 用法帮助\n \
            -l 待分析文件位置(默认为../cost_time.txt)\n\
            -s 耗时步长(默认10)\n\
            -n 需要从文件中读取多少采样数据(默认100)\n\
            "



if __name__ == '__main__':
    file_location = '../cost_time.txt'
    opts, args = getopt.getopt(sys.argv[1:], "hl:s:n:")
    data_file=""
    num =100
    for op, value in opts:
        if op == "-l":
            data_file = value
        elif op == "-s":
            try:
               value = int(value)
            except Exception, e:
                print e
                sys.exit()
            if not (type(value) == type(1) and value > 0):
                print 'Parameter -s is not a correct'
                sys.exit()
            STEP = value
        elif op == '-n':
             try:
               value = int(value)
             except Exception, e:
                print e
                sys.exit()
             if not (type(value) == type(1) and value > 0):
                print 'Parameter -n is not a correct'
                sys.exit()
             num = value
        elif op == "-h":
            usage()
            sys.exit()

    if data_file:
        file_location = data_file

    current_time, cost_time,datas = (split_data(read_data(file_location,num)))
    average = int(sum(cost_time)/len(cost_time))
    below,over =statistics_data(cost_time,average)

    max_time = max(cost_time)
    min_time = min(cost_time)
    flag = 0
    sections = []
    while flag < max_time:
        sections.append({'start':str(flag),'end':str(flag + STEP),'times':[],'rate':0})
        flag += STEP

    for item in cost_time:
        if item == 0 :
            sections[0]['times'].append(item)
        elif not item % STEP == 0:
            sections[item/STEP]['times'].append(item)
        else:
            sections[item/STEP -1]['times'].append(item)

    for section in sections:
        section['rate'] = str(round(float(len(section['times']))/float(len(cost_time))*100,1))+'%'

    print BASE_CONTENT %\
          (current_time[0],current_time[-1],len(current_time),
           max(cost_time),
           min(cost_time),int(sum(cost_time)/len(cost_time)),over,below)
    print ADVANCE_CONTENT_HEAD
    sections.reverse()
    map(print_advance ,sections)
