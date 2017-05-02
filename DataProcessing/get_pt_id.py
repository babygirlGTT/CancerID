#coding:utf-8

import csv

def iscancer(icd):
    flag = False
    with open('/home/zn/Desktop/cancer_icd9.txt', 'rb') as f:
        lines = f.readlines()
        for line in lines:
            if icd == line:
                flag = True
                break
    return flag

def get_pid():
    pid_ls = []
    with open('/home/zn/Desktop/ca_pt_id.txt', 'wb') as fout:
        with open('/home/zn/Documents/mimic/DIAGNOSES_ICD_DATA_TABLE.csv', 'rb') as fin:
            reader = csv.DictReader(fin)
            for line in reader:
                if iscancer(line['ICD9_CODE'] + '\n'):
                    num = 0
                    for id in pid_ls:
                        if line['SUBJECT_ID'] == id:
                            num += 1
                            break
                    if num == 0:
                        pid_ls.append(line['SUBJECT_ID'])

        for id in pid_ls:
            fout.write(id + '\n')

get_pid()