import multiprocessing

bind = '127.0.0.1:8001'
# 启动几个进程
wworkers = multiprocessing.cpu_count()
worder_class = 'gevent'