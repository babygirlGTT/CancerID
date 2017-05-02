import csv
import pymongo

conn = pymongo.MongoClient()
db = conn.mimic

def filter()

def insertdata(table, path, col_ls):
    table.remove()
    with open(path,'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            for col in col_ls:
                table.insert_one({col:row[col]})

diag_icd = db.DIAGNOSES_ICD
path = '/home/zn/Documents/mimic/DIAGNOSES_ICD_DATA_TABLE.csv'
col_ls = ['ROW_ID', 'SUBJECT_ID', 'ICD9_CODE']
insertdata(diagnoses, path, col_ls)

icd_diag = db.D_ICD_DIAGNOSES
path = '/home/zn/Documents/mimic/D_ICD_DIAGNOSES_DATA_TABLE.csv'
col_ls = ['ROW_ID', 'ICD9_CODE', 'SHORT_TITLE', 'LONG_TITLE']
insertdata(icd_diag, path, col_ls)

items = db.D_ITEMS
path = '/home/zn/Documents/mimic/D_ITEMS_DATA_TABLE.csv'
col_ls = ['ROW_ID', 'ITEMID', 'LABEL', 'CATEGORY']
insertdata(items, path, col_ls)

labitems = db.D_LABITEMS
path = '/home/zn/Documents/mimic/D_LABITEMS_DATA_TABLE.csv'
col_ls = ['ROW_ID', 'ITEMID', 'LABEL', 'FLUID', 'CATEGORY']
insertdata(labitems, path, col_ls)

drgcodes = db.DRGCODES
path = '/home/zn/Documents/mimic/DRGCODES_DATA_TABLE.csv'
col_ls = ['ROW_ID', 'SUBJECT_ID', 'HADM_ID', 'DESCRIPTION']
insertdata(drgcodes, path, col_ls)

labevents = db.LABEVENTS
path = '/home/zn/Documents/mimic/LABEVENTS_DATA_TABLE.csv'
col_ls = ['ROW_ID', 'SUBJECT_ID', 'ITEMID', 'VALUE', 'VALUENUM', 'VALUEUOM', 'FLAG']
insertdata(labevents, path, col_ls)

noteevents = db.NOTEEVENTS
path = '/home/zn/Documents/mimic/NOTEEVENTS_DATA_TABLE.csv'
col_ls = ['ROW_ID', 'SUBJECT_ID', 'CATEGORY', 'DESCRIPTION', 'ISERROR']
insertdata(noteevents, path, col_ls)

patients = db.PATIENTS
path = '/home/zn/Documents/mimic/PATIENTS_DATA_TABLE.csv'
col_ls = ['ROW_ID']
insertdata(patients, path, col_ls)

chartevents = db.CHARTEVENTS
path = '/media/zn/00051A0B00093CEE/mimic/CHARTEVENTS_DATA_TABLE.csv'
col_ls = ['ROW_ID']
insertdata(chartevents, path, col_ls)