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
        subid = ''
        for row in reader:
            if row['SUBJECT_ID']) == subid:
                table.insert_one({col:row[col] for col in col_ls})
            else:
                if filter(row['SUBJECT_ID']):    #筛选SUBJECT_ID
                    table.insert_one({col:row[col] for col in col_ls})  #按字段插入数据
                    subid = row['SUBJECT_ID']

def main():
    #导入表CHARTEVENTS
    charte = db.CHARTEVENTS
    path = '/media/zn/00051A0B00093CEE/mimic/CHARTEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","ITEMID","CHARTTIME","STORETIME","CGID","VALUE","VALUENUM","VALUEUOM","WARNING","ERROR","RESULTSTATUS","STOPPED"]
    importdata(charte, path, col_ls)

    

if __name__ == '__main__':
    main()