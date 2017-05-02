#coding:utf-8

import csv
import time

#suject_id = ''

with open('/home/zn/Desktop/ca_pt_id.txt', 'rb') as f:
    lines = f.readlines()

def isa(suj_id):
    flag = False
    '''if suj_id == suject_id:
        flag = True
    else:
        for line in lines:
            if suj_id == line:
                flag = True
                global suject_id
                suject_id = suj_id
                break'''
    for line in lines:
        if suj_id == line:
            flag = True
            break
    return flag

def filter(pathin, pathout, header):
    with open(pathout, 'wb') as fout:
        foutheader = header
        writer = csv.DictWriter(fout, foutheader)
        writer.writeheader()
        with open(pathin, 'rb') as fin:
            reader = csv.DictReader(fin)
            for line in reader:
                if isa(line['SUBJECT_ID'] + '\n'):
                    writer.writerow(line)

s1 = time.clock()
pathout = '/home/zn/Desktop/mimic/PATIENTS.csv'
pathin = '/home/zn/Documents/mimic/PATIENTS_DATA_TABLE.csv'
header = ['ROW_ID', 'SUBJECT_ID', 'GENDER', 'DOB', 'DOD', 'DOD_HOSP', 'DOD_SSN', 'EXPIRE_FLAG']
filter(pathin, pathout, header)
e1 = time.clock()
print str(e1 - s1)

s2 = time.clock()
pathin = '/home/zn/Documents/MIMIC/DATETIMEEVENTS_DATA_TABLE.csv'
pathout = '/home/zn/Desktop/mimic/DATETIMEEVENTS.csv'
header = ['ROW_ID', 'SUBJECT_ID', 'HADM_ID', 'ICUSTAY_ID', 'ITEMID', 'CHARTTIME', 'STORETIME', 'CGID', 'VALUE', 'VALUEUOM', 'WARNING', 'ERROR', 'RESULTSTATUS', 'STOPPED']
filter(pathin, pathout, header)
e2 = time.clock()
print str(e2 - s2)