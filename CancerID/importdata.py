#coding:utf-8

import csv
import pymongo

#连接数据库mimic
conn = pymongo.MongoClient()
db = conn.mimic

with open('/home/zn/Desktop/ca_pt_id.txt', 'rb') as f:  #打开文件，确定筛选条件
    lines = f.readlines()
    lines = [line.strip() for line in lines]

#根据条件筛选数据
def filter(subj_id):
    flag = False
    for line in lines:
        if subj_id == line:
            flag = True
            break
    return flag

#导入数据
def importdata(table, path, col_ls):
    table.remove()
    with open(path,'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if filter(row['SUBJECT_ID']):    #筛选SUBJECT_ID
                table.insert_one({col:row[col] for col in col_ls})  #按字段插入数据

#导入表ADMISSIONS
admi = db.ADMISSIONS
path = '/home/zn/Documents/MIMIC/ADMISSIONS_DATA_TABLE.csv'
col_ls = ['SUBJECT_ID', 'HADM_ID', 'ADMITTIME', 'DISCHTIME', 'MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS']
importdata(admi, path, col_ls)
