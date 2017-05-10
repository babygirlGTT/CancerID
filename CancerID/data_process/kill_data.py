# -*- coding: utf-8 -*-
'''this for data killing '''

import os
import pandas as pd

DIR_PATH = "/home/andrew/Desktop/test/"
OUT_PATH = "/home/andrew/Desktop/"

def read_files(path):
    ''' return file list '''
    f_ls = []
    for root, dirs, files in os.walk(path):
        for file_item in files:
            f_ls.append(root + file_item)
    return f_ls

FILENAMES = read_files(DIR_PATH)
j = 0
for filename in FILENAMES:
    store_index = set([1])
    with open(filename, "r") as fr:
        head = fr.readline()[:-1] # 去掉换行的第一行
        head_list = head.replace('"', '').split(',')
        for index, item in enumerate(head_list):
            if item.find('ITEMID') != -1:
                store_index.add(index)
            elif (item.find('VALUE') != -1) and (item != 'DILUTION_VALUE'):
                store_index.add(index)
            elif item.find('ERROR') != -1:
                store_index.add(index)
            elif item == 'TEXT':
                store_index.add(index)
            elif item == 'INTERPRETATION':
                store_index.add(index)
    j += 1
    fw = open(OUT_PATH + str(j) + '.csv', 'w')
    print [head_list[i] for i in store_index]
    fw.writelines(','.join([head_list[i] for i in store_index]) + '\n')
    df = pd.read_csv(filename, dtype='string', chunksize=10000)
    for chunk in df:
        header = [chunk.columns[i] for i in store_index]
        chunk.loc[:, header].to_csv(OUT_PATH + str(j) + '.csv', mode='a', header=False, index=False)
        # for line in fr:
        #     data_list = line[:-1].replace('"', '').split(',')
        #     print data_list
        #     line_to_write = ','.join([data_list[i] for i in store_index]) + '\n'
        #     fw.writelines(line_to_write)
