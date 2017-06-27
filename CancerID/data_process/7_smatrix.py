# coding:utf-8

'''
根据病人患病情况，生成病人——疾病矩阵
矩阵中病人为列，疾病为行
病人i患病j，则矩阵ij=1，否则为0
'''

import json

import pymongo


def main():
    '''main()'''
    conn = pymongo.MongoClient()
    mimic = conn.mimic
    diag = mimic.DIAGNOSES_ICD

    with open('/home/zn/Desktop/data/matrix/pid_less.txt', 'rb') as f:
        pid_ls = [i.strip() for i in f.readlines()]
    with open('/home/zn/Desktop/data/cancer_icd9.txt', 'rb') as f:
        can_code = [i.strip() for i in f.readlines()]

    dis_dic = {}
    count = 0
    for p_item in diag.find():
        if p_item['ICD9_CODE'] in can_code:
            if p_item['ICD9_CODE'] not in dis_dic:
                dis_dic[p_item['ICD9_CODE']] = count
                count += 1

    with open('/home/zn/Desktop/data/matrix/dis_dic.json', 'wb') as f:
        json.dump(dis_dic, f)

    with open('/home/zn/Desktop/data/matrix/p_dis.csv', 'wb') as f:
        for pid in pid_ls:
            ls = []
            dset = set()
            for p in diag.find({'SUBJECT_ID':pid}):
                if p['ICD9_CODE'] in dis_dic:
                    dset.add(dis_dic[p['ICD9_CODE']])
            for i in range(len(dis_dic)):
                if i in dset:
                    ls.append('1')
                else:
                    ls.append('0')
            f.write('\n' + ','.join(ls))

if __name__ == '__main__':
    main()
