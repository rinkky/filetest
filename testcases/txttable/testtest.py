#!/usr/bin/env python
# coding=utf-8

from utils import txttable

txt_file = None
def setup(file, logger):
    global txt_file
    txt_file = txttable.open_txt_table(file)
    print(txt_file)

def test_unique_first(file, logger):
    r = txttable.is_unique(txt_file,col_num=1)
    logger.test_true(r, file, "unique test")

def test_asc_first(file, logger):
    r = txttable.is_asc(txt_file,col_num=1)
    logger.test_true(r, file, "asc test")

def teardown(file, logger):
    txt_file = None
    print("teardown")
