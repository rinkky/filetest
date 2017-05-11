#!/usr/bin/env python
# coding=utf-8

class TxtTableRow(object):
    """a row of a txt table
    """
    def __init__(self, keys, values, types=[]):
        self.keys = keys
        self.types = types
        self.values = values
        self.kv = zip(keys, values)


def open_txt_table(txt_file, data_start_with=2, 
                    keys_line=0, types_line=1, 
                    split_char="\t"):
    """open txt file. return a list.

    Args:
        txt_file: path of the file.
        data_start_with: int. the data start with this row.
        keys_line: the keys are in this row.
        types_line: the types are in this row. 
            if there is no type line, make it -1.
    
    returns: a list of TxtTableRow.
    """
    file = open(txt_file,"r")
    i = 0;
    line = file.readline()
    keys = []
    types = []
    txt_table_rows = []
    while line != "":
        if(i >= data_start_with):
            values = line.split(split_char)
            txt_table_rows.append(
                TxtTableRow(keys, values, types)
            )
        elif(i==keys_line):
            keys = line.split(split_char)
        elif(i == types_line):
            types = line.split(split_char)
        i += 1
        line = file.readline()

    file.close()
    return txt_table_rows

def is_asc(table_rows, col_name="", col_num=0):
    """check if the spacific col of the table_row is asc.

    Args:
        col_name: this col to check. 
        col_num: if col_name=="", use col_num to find the col.
    """
    index = col_num
    if(col_name):
        index = table_rows[0].keys.index(col_name)
    for i in range(0, len(table_rows)-1):
        j = i+1
        if(table_rows[i].values[index] >= table_rows[j].values[index]):
            return False
    return True

def is_unique(table_rows, col_name="", col_num=0):
    """check if the spacific col of the table_row is unique.

    Args:
        col_name: this col to check. 
        col_num: if col_name=="", use col_num to find the col.
    """
    index = col_num
    if(col_name):
        index = table_rows[0].keys.index(col_name)
    tmp = {}
    for i in range(0, len(table_rows)):
        x = table_rows[i].values[index]
        if x in tmp:
            return False
        tmp[x] = i
    return True
