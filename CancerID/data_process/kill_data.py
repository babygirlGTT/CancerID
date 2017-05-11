# -*- coding: utf-8 -*-
'''this for data killing '''

import os
import pandas as pd

DIR_PATH = "/media/zn/00051A0B00093CEE/mimic/"
OUT_PATH = "/home/zn/Desktop/"

def read_files(path):
    ''' return file list '''
    f_ls = []
    for root, dirs, files in os.walk(path):
        for file_item in files:
            f_ls.append(root + file_item)
    return f_ls

FILENAMES = read_files(DIR_PATH)

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
        fw = open(OUT_PATH + filename[-25:], 'w')
        print [head_list[i] for i in store_index]
        fw.writelines(','.join([head_list[i] for i in store_index]) + '\n')
        fw.close()
    df = pd.read_csv(filename, dtype='string', chunksize=50000)
    for chunk in df:
        header = [chunk.columns[i] for i in store_index]
        chunk.loc[:, header].to_csv(OUT_PATH + filename[-25:], mode='a', header=False, index=False)
