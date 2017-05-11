#!/usr/bin/env python
# coding=utf-8

from utils import txttable

txt_file = None
def setup(file, logger):
    global txt_file
    txt_file = txttable.open_txt_table(file)

def test_unique(file, logger):
    r = txttable.is_unique(txt_file,col_num_list=[0,1])
    logger.test_true(r[0], file, "unique test"+r[1])

def test_asc(file, logger):
    r = txttable.is_asc(txt_file,col_num=0)
    logger.test_true(r[0], file, "asc test: "+r[1])

def test_not_null(file, logger):
    r = txttable.not_null(txt_file,col_name_list=["a","b","c","d"])
    logger.test_true(r[0], file, "null test: "+r[1])

def test_type(file, logger):
    r = txttable.value_type_check(txt_file)
    logger.test_true(r[0], file, "type test: "+r[1])

def teardown(file, logger):
    txt_file = None
