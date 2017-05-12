#coding:utf-8

import pymongo
import time
from datetime import datetime, time, date
import json

with open('/home/zn/Desktop/data/item_dict_final.json', 'rb') as f:
    dic = json.load(f)

def intvl_word(item, value, value_num):
    if value_num:
        num = float(value)
        if dic[item][1]:
            itvlnum = int((num - dic[item][0]) / dic[item][1])
        else:
            itvlnum = 0
        word = item + '_itvl_' + str(itvlnum)
    else:
        word = item + '_itvl_' + value
    return word

def doc_gen(tout, tin, titles, flag=''):
    if flag:
        for i in tin.find():
            doc = tout.find_one({'SUBJECT_ID':i['SUBJECT_ID']})
            doc['document'] = doc['document'] + ' ' + intvl_word(i[titles[0]], i[titles[1]], i[flag])
            tout.update({'SUBJECT_ID':i['SUBJECT_ID']}, {'$set':{'time':datetime.now(), 'document':doc['document']}})
    else:
        if tout.find_one():
            for i in tin.find():
                doc = tout.find_one({'SUBJECT_ID':i['SUBJECT_ID']})
                for title in titles:
                    doc['document'] = doc['document'] + ' ' + i[title]
                tout.update({'SUBJECT_ID':i['SUBJECT_ID']}, {'$set':{'time':datetime.now(), 'document':doc['document']}})
        else:
            for i in tin.find():
                doc = ''
                for title in titles:
                    doc = doc + ' ' + i[title]
                tout.insert_one({'SUBJECT_ID':i['SUBJECT_ID'], 'time':datetime.now(), 'document':doc})

def main():
    #连接数据库mimic
    conn = pymongo.MongoClient()
    mimic = conn.mimic
    diag = conn.diagnosis
    p_docs = diag.patient_docs
    p_docs.remove()

    patients = mimic.PATIENTS
    titles = ['GENDER']
    doc_gen(p_docs, patients, titles)

    admit = mimic.ADMISSIONS
    titles = ['MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS']
    doc_gen(p_docs, admit, titles)

    '''charte = mimic.CHARTEVENTS
    titles = ['ITEMID', 'VALUE']
    doc_gen(p_docs, charte, titles)

    labe = mimic.LABEVENTS
    titles = ['ITEMID', 'VALUE']
    doc_gen(p_docs, labe, titles)
    
    oute = mimic.OUTPUTEVENTS
    titles = ['ITEMID', 'VALUE']
    doc_gen(p_docs, oute, titles, 'VALUE')'''

if __name__ == '__main__':
    main()