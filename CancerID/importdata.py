#coding:utf-8

import csv
import pymongo

#连接数据库mimic
conn = pymongo.MongoClient()
db = conn.mimic

with open('/home/zn/Desktop/ca_pt_id.txt', 'rb') as f:  #打开文件，确定筛选条件
    lines = f.readlines()
    lines = {line.strip() for line in lines}

#根据条件筛选数据
def filter(subj_id):
    flag = False
    if subj_id in lines:
        flag = True
    return flag

#导入数据
def importdata(table, path, col_ls):
    table.remove()
    with open(path,'rb') as f:
        reader = csv.DictReader(f)
        subid = ''
        for row in reader:
            if row['SUBJECT_ID'] == subid:
                table.insert_one({col:row[col] for col in col_ls})
            else:
                if filter(row['SUBJECT_ID']):    #筛选SUBJECT_ID
                    table.insert_one({col:row[col] for col in col_ls})  #按字段插入数据
                    subid = row['SUBJECT_ID']

def main():
    #导入表ADMISSIONS
    admi = db.ADMISSIONS
    path = '/home/zn/Documents/MIMIC/ADMISSIONS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ADMITTIME","DISCHTIME","DEATHTIME","ADMISSION_TYPE","ADMISSION_LOCATION","DISCHARGE_LOCATION","INSURANCE","LANGUAGE","RELIGION","MARITAL_STATUS","ETHNICITY","EDREGTIME","EDOUTTIME","DIAGNOSIS","HOSPITAL_EXPIRE_FLAG","HAS_IOEVENTS_DATA","HAS_CHARTEVENTS_DATA"]
    importdata(admi, path, col_ls)

    #导入表CALLOUT
    call = db.CALLOUT
    path = '/home/zn/Documents/MIMIC/CALLOUT_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","SUBMIT_WARDID","SUBMIT_CAREUNIT","CURR_WARDID","CURR_CAREUNIT","CALLOUT_WARDID","CALLOUT_SERVICE","REQUEST_TELE","REQUEST_RESP","REQUEST_CDIFF","REQUEST_MRSA","REQUEST_VRE","CALLOUT_STATUS","CALLOUT_OUTCOME","DISCHARGE_WARDID","ACKNOWLEDGE_STATUS","CREATETIME","UPDATETIME","ACKNOWLEDGETIME","OUTCOMETIME","FIRSTRESERVATIONTIME","CURRENTRESERVATIONTIME"]
    importdata(call, path, col_ls)

    #导入表CHARTEVENTS
    charte = db.CHARTEVENTS
    path = '/media/zn/00051A0B00093CEE/mimic/CHARTEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","ITEMID","CHARTTIME","STORETIME","CGID","VALUE","VALUENUM","VALUEUOM","WARNING","ERROR","RESULTSTATUS","STOPPED"]
    importdata(charte, path, col_ls)

    #导入表CPTEVENTS
    cpte = db.CPTEVENTS
    path = '/home/zn/Documents/MIMIC/CPTEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","COSTCENTER","CHARTDATE","CPT_CD","CPT_NUMBER","CPT_SUFFIX","TICKET_ID_SEQ","SECTIONHEADER","SUBSECTIONHEADER","DESCRIPTION"]
    importdata(cpte, path, col_ls)

    #导入表DATETIMEEVENTS
    datetimee = db.DATETIMEEVENTS
    path = '/home/zn/Documents/MIMIC/DATETIMEEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","ITEMID","CHARTTIME","STORETIME","CGID","VALUE","VALUEUOM","WARNING","ERROR","RESULTSTATUS","STOPPED"]
    importdata(datetimee, path, col_ls)

    #导入表DIAGNOSES_ICD
    diagicd = db.DIAGNOSES_ICD
    path = '/home/zn/Documents/mimic/DIAGNOSES_ICD_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","SEQ_NUM","ICD9_CODE"]
    importdata(diagicd, path, col_ls)

    #导入表ICUSTAYS
    icu = db.ICUSTAYS
    path = '/home/zn/Documents/MIMIC/ICUSTAYS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","DBSOURCE","FIRST_CAREUNIT","LAST_CAREUNIT","FIRST_WARDID","LAST_WARDID","INTIME","OUTTIME","LOS"]
    importdata(icu, path, col_ls)

    #导入表INPUTEVENTS_MV
    inputmv = db.INPUTEVENTS_MV
    path = '/home/zn/Documents/MIMIC/INPUTEVENTS_MV_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","STARTTIME","ENDTIME","ITEMID","AMOUNT","AMOUNTUOM","RATE","RATEUOM","STORETIME","CGID","ORDERID","LINKORDERID","ORDERCATEGORYNAME","SECONDARYORDERCATEGORYNAME","ORDERCOMPONENTTYPEDESCRIPTION","ORDERCATEGORYDESCRIPTION","PATIENTWEIGHT","TOTALAMOUNT","TOTALAMOUNTUOM","ISOPENBAG","CONTINUEINNEXTDEPT","CANCELREASON","STATUSDESCRIPTION","COMMENTS_EDITEDBY","COMMENTS_CANCELEDBY","COMMENTS_DATE","ORIGINALAMOUNT","ORIGINALRATE"]
    importdata(inputmv, path, col_ls)

    #导入表INPUTEVENTS_CV
    inputcv = db.INPUTEVENTS_CV
    path = '/home/zn/Documents/MIMIC/INPUTEVENTS_CV_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","CHARTTIME","ITEMID","AMOUNT","AMOUNTUOM","RATE","RATEUOM","STORETIME","CGID","ORDERID","LINKORDERID","STOPPED","NEWBOTTLE","ORIGINALAMOUNT","ORIGINALAMOUNTUOM","ORIGINALROUTE","ORIGINALRATE","ORIGINALRATEUOM","ORIGINALSITE"]
    importdata(inputcv, path, col_ls)

    #导入表LABEVENTS
    labe = db.LABEVENTS
    path = '/home/zn/Documents/mimic/LABEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ITEMID","CHARTTIME","VALUE","VALUENUM","VALUEUOM","FLAG"]
    importdata(labe, path, col_ls)

    #导入表MICROBIOLOGYEVENTS
    microbe = db.MICROBIOLOGYEVENTS
    path = '/home/zn/Documents/MIMIC/MICROBIOLOGYEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","CHARTDATE","CHARTTIME","SPEC_ITEMID","SPEC_TYPE_DESC","ORG_ITEMID","ORG_NAME","ISOLATE_NUM","AB_ITEMID","AB_NAME","DILUTION_TEXT","DILUTION_COMPARISON","DILUTION_VALUE","INTERPRETATION"]
    importdata(microbe, path, col_ls)

    #导入表NOTEEVENTS
    notee = db.NOTEEVENTS
    path = '/home/zn/Documents/mimic/NOTEEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","CHARTDATE","CHARTTIME","STORETIME","CATEGORY","DESCRIPTION","CGID","ISERROR","TEXT"]
    importdata(notee, path, col_ls)

    #导入表OUTPUTEVENTS
    outpute = db.OUTPUTEVENTS
    path = '/home/zn/Documents/MIMIC/OUTPUTEVENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","CHARTTIME","ITEMID","VALUE","VALUEUOM","STORETIME","CGID","STOPPED","NEWBOTTLE","ISERROR"]
    importdata(outpute, path, col_ls)

    #导入表PATIENTS
    patients = db.PATIENTS
    path = '/home/zn/Documents/mimic/PATIENTS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","GENDER","DOB","DOD","DOD_HOSP","DOD_SSN","EXPIRE_FLAG"]
    importdata(patients, path, col_ls)

    #导入表PRESCRIPTIONS
    presc = db.PRESCRIPTIONS
    path = '/home/zn/Documents/MIMIC/PRESCRIPTIONS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","STARTDATE","ENDDATE","DRUG_TYPE","DRUG","DRUG_NAME_POE","DRUG_NAME_GENERIC","FORMULARY_DRUG_CD","GSN","NDC","PROD_STRENGTH","DOSE_VAL_RX","DOSE_UNIT_RX","FORM_VAL_DISP","FORM_UNIT_DISP","ROUTE"]
    importdata(presc, path, col_ls)

    #导入表PROCEDUREEVENTS_MV
    procede = db.PROCEDUREEVENTS_MV
    path = '/home/zn/Documents/MIMIC/PROCEDUREEVENTS_MV_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","STARTTIME","ENDTIME","ITEMID","VALUE","VALUEUOM","LOCATION","LOCATIONCATEGORY","STORETIME","CGID","ORDERID","LINKORDERID","ORDERCATEGORYNAME","SECONDARYORDERCATEGORYNAME","ORDERCATEGORYDESCRIPTION","ISOPENBAG","CONTINUEINNEXTDEPT","CANCELREASON","STATUSDESCRIPTION","COMMENTS_EDITEDBY","COMMENTS_CANCELEDBY","COMMENTS_DATE"]
    importdata(procede, path, col_ls)

    #导入表PROCEDURES_ICD
    proceicd = db.PROCEDURES_ICD
    path = '/home/zn/Documents/MIMIC/PROCEDURES_ICD_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","SEQ_NUM","ICD9_CODE"]
    importdata(proceicd, path, col_ls)

    #导入表SERVICES
    services = db.SERVICES
    path = '/home/zn/Documents/MIMIC/SERVICES_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","TRANSFERTIME","PREV_SERVICE","CURR_SERVICE"]
    importdata(services, path, col_ls)

    #导入表TRANSFERS
    transfer = db.TRANSFERS
    path = '/home/zn/Documents/MIMIC/TRANSFERS_DATA_TABLE.csv'
    col_ls = ["SUBJECT_ID","HADM_ID","ICUSTAY_ID","DBSOURCE","EVENTTYPE","PREV_CAREUNIT","CURR_CAREUNIT","PREV_WARDID","CURR_WARDID","INTIME","OUTTIME","LOS"]
    importdata(transfer, path, col_ls)

if __name__ == '__main__':
    main()