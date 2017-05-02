import csv
import pymongo

#连接数据库mimic
conn = pymongo.MongoClient()
db = conn.mimic

#导入数据
def importdata(table, path, col_ls):
    table.remove()
    with open(path,'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            table.insert_one({col:row[col] for col in col_ls})  #按字段插入数据

#导入表ADMISSIONS
admi = db.ADMISSIONS
path = '/home/zn/Documents/MIMIC/ADMISSIONS_DATA_TABLE.csv'
col_ls = ['SUBJECT_ID', 'HADM_ID', 'ADMITTIME', 'DISCHTIME', 'MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS']
insertdata(admi, path, col_ls)

