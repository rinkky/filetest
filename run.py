#!/usr/bin/env python
# coding=utf-8
import Queue
import glob
import time

import config
import filetest
from filetest import LogThread
import testlog

for item in config.collection:
    models= item["models"]
    files = []
    for x in item["files"]:
        files += glob.glob(x)
    name = item["name"]
    log_queue = Queue.Queue(100)
    log_thread = LogThread(log_queue, name+".log")
    log_thread.daemon = True
    log_thread.start()

    filetest.run_test_by_model(name, models, files, log_queue)
    while not log_queue.empty():
        time.sleep(1)
