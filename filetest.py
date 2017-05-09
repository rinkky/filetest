#!/usr/bin/env python
# coding=uft-8

def run_test(methods, path, queue_log):
    """Run a series of testcase.

    Run the testcases in methods.

    Args:
        methods: a string list to store all the function name. the first 
            element is a flag.
        path: the folder that contains the files to be tested.
        queue_log: a queue to cache log.
    """
    if methods is None or len(methods) < 2:
        raise ValueError("Error: methods invalid. ")
    flag = methods[0]
    methods.pop(0)
    for method in methods:
        eval(method)(path, queue_log)

