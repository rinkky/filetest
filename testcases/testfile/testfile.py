#/usr/bin/env python
# coding=utf-8

import os

def setup(path, logger):
    """setup
    """
    pass

def test_nomal_file(path, logger):
    """nomal test
    """
    max_size = 60 #bytes
    min_size = 0
    size = os.path.getsize(path) #bytes
    
    logger.test_bigger(
        size, min_size, path, 
        "file size is {0} bytes, min is {1}".format(size, min_size)
    )
    logger.test_bigger(
        max_size, size, path, 
        "file size is {0} bytes, max is {1}".format(size, max_size)
    )

def teardown(path, logger):
    """teardown
    """
    pass
