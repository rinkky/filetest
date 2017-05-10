#!/usr/bin/env python
# coding=utf-8

import os
import threading
import time
from testlog import TestLog
import testcases.testfile.testfile


class LogThread(threading.Thread):
    """the thread to handle logs

    you can use this to print log and save log files.
    or you can make your own tread to deal with log.
    """
    def __init__(self, log_queue, log_file):
        threading.Thread.__init__(self)
        self._log_queue = log_queue
        self.log_file = log_file
        self.file_stream = open(log_file, "a")
        self.daemon = True

    def run(self):
        while True:
            if(self._log_queue.empty()):
                time.sleep(1)
                continue
            log = self._log_queue.get(False)
            print(log)
            self.file_stream.write(log+"\n")
        self.file_stream.close()


def run_test(test_name, methods, files, log_queue, is_file_first=True):
    """Run a series of testcase.

    Run the testcases in methods.

    Args:
        test_name: a string to sign this test.

        methods: a string list to store all the function name.
        
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
        "\n\n[begin]"
        +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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
    logger.normallog(
        "[end]"
        +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        +"------------------"
    )

def run_test_by_model(test_name, models, files, log_queue):
    """Run a series of testcase.

    Run the testcases in models.

    Args:
        test_name: a string to sign this test.

        models: a string list to store all the model name. 
            function setup() will run first.
            then function like test_*() will run.
            function teardown() will run last. 
        
        files: a list of files to be tested.
        
        log_queue: a queue to cache log.
        
        is_file_first: default True. 
            if True, run all tests on a file, then test another.
            if False, run a test on all file, then run another test.
    """
    methods = ["setup"]
    for model in models:
        methods += [x for x in dir(eval(model)) if x.startswith("test_")]


    logger = TestLog(log_queue, test_name)
    logger.normallog(
        "\n\n[begin]"
        +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        +"------------------"
    )
