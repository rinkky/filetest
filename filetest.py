#!/usr/bin/env python
# coding=utf-8

import os
import threading
import time
from testlog import TestLog
import testcases.testfile.testfile
import testcases.txttable
import testcases.txttable.testtest
from utils import *

class LogThread(threading.Thread):
    """the thread to handle logs
    """
    def __init__(self, log_queue, log_file, fail_only=True):
        threading.Thread.__init__(self)
        self._log_queue = log_queue
        self.log_file = log_file
        self.file_stream = open(log_file, "a")
        self.daemon = True
        self.fail_only = fail_only

    def run(self):
        while True:
            if(self._log_queue.empty()):
                time.sleep(1)
                continue
            log = self._log_queue.get(False)
            print(log)
            if(self.fail_only == True and log.startswith("[PASS]")):
                continue
            self.file_stream.write(log+"\n")
            if(log.startswith("[end]")):
                break
        self.file_stream.close()


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

def run_test_by_model(test_name, models, files, log_queue):
    """Run a series of testcase.

    Run the testcases in models. always file_first

    Args:
        test_name: a string to sign this test.

        models: a string list to store all the model name. 
            function setup() will run first.
            then function like test_*() will run.
            function teardown() will run last. 
        
        files: a list of files to be tested.
        
        log_queue: a queue to cache log.
        
    """
    logger = TestLog(log_queue, test_name)
    logger.normallog(
        "\n\n[begin]"
        +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        +"------------------"
    )

    for file in files:
        for model in models:
            #eval(method)(file, logger)
            attrs = dir(eval(model))
            if("setup" in attrs):
                eval(model + ".setup")(file, logger)
            for x in attrs:
                if x.startswith("test_"):
                    eval(model+"."+x)(file, logger)
            if("teardown" in attrs):
                eval(model + ".teardown")(file, logger)

    logger.normallog(
        "[end]"
        +time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        +"------------------"
    )
