import multiprocessing

bind = '0.0.0.0:8080'
multiprocessing.cpu_count() * 2 + 1
timeout = 300
accesslog = '-'
