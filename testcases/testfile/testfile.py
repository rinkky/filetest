#/usr/bin/env python
# coding=utf-8

import os

def test_nomal_file(path, logger):
	"""nomal test
	"""
	max_size = 1000 #bytes
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
