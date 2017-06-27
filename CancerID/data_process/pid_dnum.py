# coding:utf-8

import json

import pymongo


def main():
    conn = pymongo.MongoClient()
    mimic = conn.mimic
    diag = mimic.DIAGNOSES_ICD

    with open('/home/zn/Desktop/data/ca_pt_id.txt', 'rb') as f:
        pid_ls = [i.strip() for i in f.readlines()]
    with open('/home/zn/Desktop/data/cancer_icd9.txt', 'rb') as f:
        can_code = [i.strip() for i in f.readlines()]

    dis_dic = {}
    ls = []
    sl = []
    for pid in pid_ls:
        dis = {}
        for p in diag.find({'SUBJECT_ID':pid}):
            if p['ICD9_CODE'] in can_code:
                dis[p['ICD9_CODE']] = ''
        if len(dis) <= 3:
            ls.append(pid)
        else:
            sl.append(pid)

    with open('/home/zn/Desktop/data/matrix/pid_less.txt', 'wb') as f:
        f.write('\n'.join(ls))
    with open('/home/zn/Desktop/data/matrix/pid_more.txt', 'wb') as f:
        f.write('\n'.join(sl))


if __name__ == '__main__':
    main()
