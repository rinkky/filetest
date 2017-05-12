#!/usr/bin/env python
# coding=utf-8

import Queue
import glob
import time
import os

from config import config
import filetest
from testlog import LogThread
import testlog

log_folder = os.path.join(
    config.log_base_path, 
    time.strftime("%y-%m-%d_%H.%M.%S")
)
if(not os.path.exists(log_folder)):
    os.makedirs(log_folder)

for item in config.collection:
    models= item["models"]
    files = []
    for x in item["files"]:
        files += glob.glob(x)
    name = item["name"]
    log_path = os.path.join(
        log_folder,
        name+".log"
    )
    log_queue = Queue.Queue(100)
    log_thread = LogThread(log_queue, log_path)
    log_thread.daemon = True

    #deal with log
    log_thread.start()
    
    #run test
    filetest.run_test_by_model(name, models, files, log_queue)

    #wait until all logs are deal with
    while not log_queue.empty():
        time.sleep(1)
