#!encoding=utf-8
ws_url = "http://basews.shop.letv.com/services/OpenSku/querySkuForBill.do?skuNo=600400002836"
sampling_count = 2
# 监控10分钟运行一次
interval = 10
data_txt_location = "data.txt"
data_txt_separator = "##"
success_flag='"code":200'
success_flag_old='message'
max_fail = 2
max_timeout = 1000
to_list = ['sunwei3@le.com']
#,'lijianzhong@le.com','hjuji@letv.com'
# 使用linux定时任务crontab
use_crontab = False
#post方法，持久化每次调用耗时到文件
post_persist_location = 'cost_time.txt'
