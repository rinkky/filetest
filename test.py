#!/usr/bin/env python
# coding=utf-8
import Queue
import time

import filetest
from filetest import LogThread
from testlog import TestLog 
import testcases.testfile.testfile

#eval("testcases.testfile.testfile.__name__")

methods = ["testcases.testfile.testfile.test_nomal_file"]
files = ["testlog.py"]

log_queue = Queue.Queue(100)

log_thread = LogThread(log_queue,"test.log")
log_thread.start()

filetest.run_test("testtest", methods, files, log_queue)

while not log_queue.empty():
	time.sleep(1)
	
print("exit") 