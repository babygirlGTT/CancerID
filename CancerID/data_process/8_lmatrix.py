# coding:utf-8
'''共病疾病矩阵'''

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
    for pid in pid_ls:
        dis = {}
        for p in diag.find({'SUBJECT_ID':pid}):
            if p['ICD9_CODE'] in can_code:
                dis[p['ICD9_CODE']] = ''
        if len(dis) <= 3:
            flag = 0
            for i in range(len(dis_dic)):
                if dis_dic[i] == dis:
                    flag = 1
                    break
            if flag == 0:
                dis_dic[count] = dis
                print count
                count += 1

    with open('/home/zn/Desktop/data/matrix/dis_dic_comb.json', 'wb') as f:
        json.dump(dis_dic, f)

    with open('/home/zn/Desktop/data/matrix/p_dis_comb.csv', 'wb') as f:
        ls = []
        for pid in pid_ls:
            dis = {}
            for p in diag.find({'SUBJECT_ID':pid}):
                if p['ICD9_CODE'] in can_code:
                    dis[p['ICD9_CODE']] = ''
            if len(dis) <= 3:
                for i in dis_dic:
                    if dis_dic[i] == dis:
                        print i
                        ls.append(str(i))
                        break
        f.write('\n'.join(ls))

if __name__ == '__main__':
    main()
