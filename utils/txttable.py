#!/usr/bin/env python
# coding=utf-8

import re

class TxtTableRow(object):
    """a row of a txt table
    """
    def __init__(self, keys, values, types=[]):
        self.keys = keys
        self.types = types
        self.values = values
        self.kv = dict(zip(keys, values))


def open_txt_table(txt_file, data_start_with=2,keys_line=0, types_line=1, split_char="\t"):
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
        line = line.strip("\n")
        line = line.strip("\r")
        if(i >= data_start_with):
            values = line.split(split_char)
            n = len(values)
            values += [" " for x in range(len(keys) - n)]
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
    rst = True
    lst = []
    if(col_name):
        index = table_rows[0].keys.index(col_name)
    for i in range(0, len(table_rows)-1):
        j = i+1
        value1 = table_rows[i].values[index]
        value2 = table_rows[j].values[index]
        if(value1 >= value2):
            rst = False
            lst.append("(col:{0},row:{1},value:{2})".format(
                index,j,value2
            ))
    return rst,",".join(lst)

def is_unique(table_rows, col_name_list=[], col_num_list=[]):
    """check if the spacific col of the table_row is unique.

    Args:
        col_name_list: these cols to check.  
        col_num_list: if col_name_list=[], use col_num_list.
    
    return: like (True, "") or like 
        (False,"(col:id,row:3,value:78),(col:name,row:6,value:jyc)")
    """
    keys = col_name_list
    if(not keys):
        keys = [table_rows[0].keys[x] for x in col_num_list]

    rst = True
    lst = []
    for key in keys:
        tmp = {}
        for i in range(0, len(table_rows)):
            value = table_rows[i].kv[key]
            if value in tmp:
                rst = False
                lst.append("(col:{0},row:{1},value:{2})".format(
                    key,i,value
                ))
            tmp[value] = i

    return rst,",".join(lst)

def value_type_check(table_rows):
    """check the types and values. if not match, return False

    Args:
        table_rows: a list of TxtTableRow

    return: if any type and value not match, return False.
    """
    types = table_rows[0].types
    rst = True
    lst = []
    row_num = 0
    for row in table_rows:
        for i in range(0, len(row.values)):
            data_type = types[i].strip().upper()
            if(data_type == "INT"):
                if(not _is_int(row.values[i])):
                    rst = False
                    lst.append("(col:{0},row:{1},value:{2})".format(
                        i, row_num, row.values[i]
                    ))

            elif(data_type == "FLOAT"):
                if(not _is_float(row.values[i])):
                    rst = False
                    lst.append("(col:{0},row:{1},value:{2})".format(
                        i, row_num, row.values[i]
                    ))
        row_num += 1
    return rst,",".join(lst)

def not_null(table_rows, col_name_list=[], col_num_list=[]):
    """if the specific cols have any null value. return False

    Args:
        table_rows: a row list of TxtTableRow.
        col_name_list: a list of string. rows names.
        col_num_list: a list of int. 
            if col_name_list == [], use col_num_list.

    return: if there is any null value, return False.
    """
    keys = col_name_list
    rst = True
    lst = []
    if(not keys): #key == [] or key == None
        keys = [table_rows[0].keys[x] for x in col_num_list]

    row_num = 0
    for row in table_rows:
        for key in keys:
            if(row.kv[key].strip() == ""):
                rst = False
                lst.append("(col:{0},row:{1},value:{2})".format(
                    key, row_num, row.kv[key].strip()
                ))
        row_num += 1
    return rst,",".join(lst)

def _is_int(_str):
    p = re.compile(r"\d+$")
    return (p.match(_str.strip()) != None)

def _is_float(_str):
    p = re.compile(r"\d+(\.\d+)?")
    return (p.match(_str.strip()) != None)

