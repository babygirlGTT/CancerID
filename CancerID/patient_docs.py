#coding:utf-8

import pymongo
import time
from datetime import datetime, time, date

def doc_gen(tout, tin, ls, key=None):
    if tout.find_one():
        for i in tin.find():
            doc = tout.find_one({'SUBJECT_ID':i['SUBJECT_ID']})
            for title in ls:
                doc['document'] = doc['document'] + ' ' + i[title]
            tout.update({'SUBJECT_ID':i['SUBJECT_ID']}, {'$set':{'time':datetime.now(), 'document':doc['document']}})
    else:
        for i in tin.find():
            doc = ''
            for title in ls:
                doc = doc + ' ' + i[title]
            tout.insert_one({'SUBJECT_ID':i['SUBJECT_ID'], 'time':datetime.now(), 'document':doc})


def main():
    #连接数据库mimic
    conn = pymongo.MongoClient()
    mimic = conn.mimic
    test = conn.test
    P_docs = test.patient_docs
    P_docs.remove()

    patients = mimic.PATIENTS
    titles = ['GENDER']
    doc_gen(P_docs, patients, titles)

    admit = mimic.ADMISSIONS
    titles = ['MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS']
    doc_gen(P_docs, admit, titles)

    charte = mimic.CHARTEVENTS
    titles = ['ITEMID', 'VALUE']
    doc_gen(P_docs, charte, titles)

    labe = mimic.LABEVENTS
    titles = ['ITEMID', 'VALUE']
    doc_gen(P_docs, labe, titles)
    
    oute = mimic.OUTPUTEVENTS
    titles = ['ITEMID', 'VALUE']
    doc_gen(P_docs, oute, titles)

if __name__ == '__main__':
    main()