#coding:utf-8

import csv
import json

#与列表数值比较并替换
def compare(ls, num):
    flag = 0
    for n in ls[1]:
        if n == num:
            flag = 1
            break
    if flag:
        ls[1].append(num)
        if num < ls[0][0]:
            ls[0][0] = num
        elif num > ls[1]:
            ls[0][1] = num
    return ls

def dict_gen(dic, f, ):
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
    dic = dict_gen()
    with open('/home/zn/Desktop/data/item_dict.json', 'wb') as f:
        json.dump(dic, f)   #存入json文件

if __name__ == '__main__':
    main()