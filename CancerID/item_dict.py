#coding:utf-8

import csv
import json
import time

#与列表数值比较并替换
def compare(d, num):
    d['nums'].add(num)
    if num < d['min']:
        d['min'] = num
    elif num > d['max']:
        d['max'] = num
    return d

def dict_gen(dic, fn, id='ITEMID',key='VALUENUM'):
    with open(fn, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row[key]: #判断VALUENUM是否为空
                if row[id] in dic.keys():   #判断是否存在于字典中
                    dic[row[id]] = compare(dic[row[id]], float(row[key]))   #比较数值，更新字典
                else:
                    s = set([float(row[key])])
                    dic[row[id]] = {'min':float(row[key]), 'max':float(row[key]), 'nums':s}   #存入字典
    return dic

def dict_gen_(dic, f, value):
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

    fn = '/home/zn/Desktop/LABEVENTS_DATA_TABLE.csv'
    dic = dict_gen(dic, fn)
    e = time.time()
    print e-s

    fn = '/home/zn/Desktop/OUTPUTEVENTS_DATA_TABLE.csv'
    dic = dict_gen(dic, fn, key='VALUE')
    e = time.time()
    print e-s

    for key in dic.keys():
        dic[key]['nums'] = list(dic[key]['nums'])
    with open('/home/zn/Desktop/data/item_dict.json', 'wb') as f:
        json.dump(dic, f)   #存入json文件

if __name__ == '__main__':
    main()