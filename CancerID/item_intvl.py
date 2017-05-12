#coding:utf-8

import math
import json

def intvl_change(dic):
    for key in dic.keys():
        itvl_num = int(math.log(len(dic[key]['nums']), 2)) + 1
        itvl_len = (dic[key]['max'] - dic[key]['min']) / itvl_num
        dic[key]['itvl_num'] = itvl_num
        dic[key]['itvl_len'] = itvl_len
        dic[key].pop('nums')
    return dic

def main():
    with open('/home/zn/Desktop/data/item_dict.json', 'rb') as f:
        dic = json.load(f)
    dic = intvl_change(dic)
    with open('/home/zn/Desktop/data/item_dict_final.json', 'wb') as f:
        json.dump(dic, f)

if __name__ == '__main__':
    main()