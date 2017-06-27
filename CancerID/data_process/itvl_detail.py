# coding:utf-8

import json
import re

from pymongo import MongoClient


def word_detail(word):
    '''将item的造词释义'''
    with open('/home/zn/Desktop/data/item_dict_final.json', 'rb') as f:
        item_dic = json.load(f)
    items_label = MongoClient('118.89.186.110', 27017).diagnosis.d_items.find_one()

    detail = ''
    print re.findall(r'\d+_itvl', word)
    if re.findall(r'\d+_itvl', word):
        item_id = re.findall(r'\d+', word)[0]
        item_label = items_label[item_id]
        value = ''
        if re.findall(r'itvl_\d+', word):
            itvl = int(re.findall(r'\d+', word)[1])
            min_num = item_dic[item_id]['min'] + item_dic[item_id]['itvl_len'] * itvl
            max_num = item_dic[item_id]['min'] + item_dic[item_id]['itvl_len'] * (itvl + 1)
            value = '%.2f~%.2f' % (min_num, max_num)
        else:
            value = re.findall(r'itvl_\w*', word)[0][5:]
        detail = item_label + ':' + value
    else:
        detail = word

    return detail

def main():
    '''main()'''
    print word_detail('226559_itvl_0')

if __name__ == '__main__':
    main()
