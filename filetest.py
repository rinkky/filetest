#!/usr/bin/env python
# coding=utf-8

import os
import threading
import time
from testlog import TestLog
import testcases.testfile.testfile


class LogThread(threading.Thread):
    """the thread to handle logs
    """
    def __init__(self, log_queue, log_file):
        threading.Thread.__init__(self)
        self._log_queue = log_queue
        self.running = False
        self.log_file = log_file
        self.file_stream = open(log_file, "a")

    def run(self):
        self.running = True

        while self.running:
            if(self._log_queue.empty()):
                time.sleep(1)
                continue
            log = self._log_queue.get(False)
            print(log)
            self.file_stream.write(log+"\n")
        self.file_stream.close()

    def stop(self):
        self.running = False


def run_test(test_name, methods, files, log_queue, is_file_first=True):
    """Run a series of testcase.

    Run the testcases in methods.

    Args:
        test_name: a string to sign this test.

        methods: a string list to store all the function name. the first 
            element is a flag.
        
        files: a list of files to be tested.
        
        log_queue: a queue to cache log.
        
        is_file_first: default True. 
            if True, run all tests on a file, then test another.
            if False, run a test on all file, then run another test.
    """
    if methods is None or len(methods) < 1:
        raise ValueError("Error: methods invalid. ")

    logger = TestLog(log_queue, test_name)

    logger.normallog(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        +"------------------"
    )
    if(is_file_first):
        for file in files:
            for method in methods:
                eval(method)(file, logger)
    else:
        for method in methods:
            for file in files:
                eval(method)(file, logger)

