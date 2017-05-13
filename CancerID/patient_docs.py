#coding:utf-8

import pymongo
from datetime import datetime, time, date
import time
import json

with open('/home/zn/Desktop/data/item_dict_final.json', 'rb') as f:
    dic = json.load(f)

def intvl_word(item, value, value_num):
    if value_num:
        num = float(value_num)
        if dic[item]['itvl_len'] != 0:
            itvlnum = int((num - dic[item]['min']) / dic[item]['itvl_len'])
        else:
            itvlnum = 0
        word = item + '_itvl_' + str(itvlnum)
    else:
        word = item + '_itvl_' + value
    return word

def doc_gen(docs, tin, titles, flag=''):
    if flag:
        cursor = tin.find(no_cursor_timeout = True)
        count = 0
        n = 0
        ts = time.time()
        for ti in cursor:
            docs[ti['SUBJECT_ID']] = docs[ti['SUBJECT_ID']] + ' ' + intvl_word(ti[titles[0]], ti[titles[1]], ti[flag])
            count +=1
            if count%1000000 == 0:
                n +=1
                te = time.time()
                print '\t', n, te-ts
                ts = time.time()
        cursor.close()
    else:
        if docs:
            for ti in tin.find():
                for title in titles:
                    docs[ti['SUBJECT_ID']] = docs[ti['SUBJECT_ID']] + ' ' + ti[title]
        else:
            for ti in tin.find():
                doc = ''
                for title in titles:
                    doc = doc + ' ' + ti[title]
                docs[ti['SUBJECT_ID']] = doc
    return docs

def main():
    conn = pymongo.MongoClient()
    mimic = conn.mimic

    docs = {}
    s = time.time()
    patients = mimic.PATIENTS
    titles = ['GENDER']
    docs = doc_gen(docs, patients, titles)
    e = time.time()
    print e-s

    s = time.time()
    admit = mimic.ADMISSIONS
    titles = ['MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS']
    docs = doc_gen(docs, admit, titles)
    e = time.time()
    print e-s

    s = time.time()
    oute = mimic.OUTPUTEVENTS
    titles = ['ITEMID', 'VALUE']
    docs = doc_gen(docs, oute, titles, 'VALUE')
    e = time.time()
    print e-s

    s = time.time()
    labe = mimic.LABEVENTS
    titles = ['ITEMID', 'VALUE']
    docs = doc_gen(docs, labe, titles, 'VALUENUM')
    with open('/home/zn/Desktop/doc.json', 'wb') as f:
        json.dump(docs, f)
    e = time.time()
    print e-s

    s = time.time()
    charte = mimic.CHARTEVENTS
    titles = ['ITEMID', 'VALUE']
    docs = doc_gen(docs, charte, titles, 'VALUENUM')
    with open('/home/zn/Desktop/doc.json', 'wb') as f:
        json.dump(docs, f)
    e = time.time()
    print e-s

    s = time.time()
    diag = conn.diagnosis
    p_docs = diag.patient_docs
    p_docs.remove()
    for u in docs:
        p_docs.insert_one({'SUBJECT_ID':u, 'time':datetime.now(), 'document':docs[u]})
    e = time.time()
    print e-s

if __name__ == '__main__':
    main()
