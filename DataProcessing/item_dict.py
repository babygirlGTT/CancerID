#coding:utf-8

import csv
import json

#与列表数值比较并替换
def compare(ls, num):
    if num < ls[0]:
        ls[0] = num
    elif num > ls[1]:
        ls[1] = num
    return ls

def item():
    dic = {}
    with open('/home/zn/Documents/CHARTEVENTS.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['VALUENUM']: #判断VALUENUM是否为空
                if row['ITEMID'] in dic.keys():   #判断是否存在于字典中
                    dic[row['ITEMID']] = compare(dic[row['ITEMID']], float(row['VALUE']))   #比较数值
                else:
                    dic[row['ITEMID']] = [float(row['VALUE']), float(row['VALUE'])]   #存入字典
    with open('/home/zn/Desktop/data/item_dict.json', 'wb') as f:
        json.dump(dic, f)   #存入json文件

def main():
    item()

if __name__ == '__main__':
    main()