#!/usr/bin/env python
# coding=utf-8

import os
from testlog import TestLog

def run_test(test_name, methods, path, queue_log, is_file_first=True):
    """Run a series of testcase.

    Run the testcases in methods.

    Args:
        test_name: a string to sign this test.

        methods: a string list to store all the function name. the first 
            element is a flag.
        
        path: the folder that contains the files to be tested.
        
        queue_log: a queue to cache log.
        
        is_file_first: default True. 
            if True, run all tests on a file, then test another.
            if False, run a test on all file, then run another test.
    """
    if methods is None or len(methods) < 2:
        raise ValueError("Error: methods invalid. ")
    if (not os.path.isdir(path)):
        raise ValueError("Error: path invalid. it is not a dir")

    logger = TestLog(queue_log, test_name)

    if(is_file_first):
        for file in os.listdir(path):
            for method in methods:
                eval(method)(path, logger)

    else:
        for method in methods:
            for file in os.listdir(path):
                eval(method)(path, logger)