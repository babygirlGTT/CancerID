#coding:utf-8

import csv
import json
import time

#与列表数值比较并替换
def compare(ls, num):
    ls[1].add(num)
    if num < ls[0][0]:
        ls[0][0] = num
    elif num > ls[1]:
        ls[0][1] = num
    return ls

def dict_gen(dic, fn, id='ITEMID',key='VALUENUM'):
    with open(fn, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[key]: #判断VALUENUM是否为空
                if row[id] in dic.keys():   #判断是否存在于字典中
                    dic[row[id]] = compare(dic[row[id]], float(row[key]))   #比较数值，更新字典
                else:
                    s = set([float(row[key])])
                    dic[row[id]] = [[float(row[key]), float(row[key])], s]   #存入字典
    return dic

def dict_gen(dic, f, value):
    with open('/home/zn/Documents/CHARTEVENTS.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['VALUENUM']: #判断VALUENUM是否为空
                if row['ITEMID'] in dic.keys():   #判断是否存在于字典中
                    dic[row['ITEMID']] = compare(dic[row['ITEMID']], float(row['VALUE']))   #比较数值，更新字典
                else:
                    dic[row['ITEMID']] = [[float(row['VALUE']), float(row['VALUE'])], [float(row['VALUE'])]]   #存入字典
    return dic


def main():
    s = time.time()
    dic = {}

    fn = '/media/zn/00051A0B00093CEE/mimic/CHARTEVENTS_DATA_TABLE.csv'
    dic = dict_gen(dic, fn)
    e = time.time()
    print e-s

    fn = '/home/zn/Documents/mimic/LABEVENTS_DATA_TABLE.csv'
    dic = dict_gen(dic, fn)
    e = time.time()
    print e-s

    fn = '/home/zn/Documents/mimic/MICROBIOLOGYEVENTS_DATA_TABLE.csv'
    dic = dict_gen(dic, fn, id='SPEC_ITEMID', key='DILUTION_VALUE')
    e = time.time()
    print e-s

    fn = '/home/zn/Documents/mimic/OUTPUTEVENTS_DATA_TABLE.csv'
    dic = dict_gen(dic, fn, key='VALUE')
    e = time.time()
    print e-s

    for key in dic.keys():
        dic[key] = [dic[key][0], list(dic[key][1])]
    with open('/home/zn/Desktop/data/item_dict.json', 'wb') as f:
        json.dump(dic, f)   #存入json文件

if __name__ == '__main__':
    main()