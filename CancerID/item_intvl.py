#coding:utf-8

import math
import json

def intvls(bound, nums):
    ivnum = int(math.log(len(nums), 2))
    ls = [bound[0]]
    if ivnum:
        l = (bound[1]-bound[0])/(ivnum+1)
        for i in range(ivnum):
            ls.append(ls[i] + l)
        ls.append(bound[1])
    else:
        ls.append(bound[1])
    return ls

def intvl_change(dic):
    for key in dic.keys():
        dic[key] = intvls(dic[key][0], dic[key][1])
    return dic

def main():
    with open('/home/zn/Desktop/data/item_dict.json', 'rb') as f:
        dic = json.load(f)
    dic = intvl_change(dic)
    with open('/home/zn/Desktop/data/item_dict_final.json', 'wb') as f:
        dic = json.dump(dic, f)

if __name__ == '__main__':
    main()