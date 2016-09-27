import multiprocessing

# bind adrress
bind = '0.0.0.0:8080'
forwarded_allow_ips = '*'

# reload workers on code change (usefull for development)
reload = True

# logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# worker class
worker_class = 'aiohttp.worker.GunicornWebWorker'

# workers / timeout
timeout = 120
workers = multiprocessing.cpu_count() * 2 + 1

