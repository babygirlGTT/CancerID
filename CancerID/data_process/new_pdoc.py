# coding:utf-8

import json
import re

from datetime import datetime
from pymongo import MongoClient


def new_pdoc(patient_id):
    '''读取病人ID为patient_id的数据，形成文档'''

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

    def get_word(item, value):
        word = ''
        if value:
            word = item + '_itvl_' + value
        return word

    def doc_gen(docs, tin, titles, flag=''):
        if flag:
            for ti in tin.find({'SUBJECT_ID':patient_id}):
                docs[patient_id] = docs[patient_id] + ' ' + intvl_word(ti[titles[0]], ti[titles[1]], ti[flag])
        else:
            if docs:
                for ti in tin.find({'SUBJECT_ID':patient_id}):
                    for title in titles:
                        docs[patient_id] = docs[patient_id] + ' ' + ti[title]
            else:
                for ti in tin.find({'SUBJECT_ID':patient_id}):
                    doc = ''
                    for title in titles:
                        doc = doc + ' ' + ti[title]
                    docs[patient_id] = doc
        return docs

    conn = MongoClient('118.89.186.110', 27017)
    mimic = conn.test
    patients = mimic.PATIENTS
    admit = mimic.ADMISSIONS
    oute = mimic.OUTPUTEVENTS
    labe = mimic.LABEVENTS
    charte = mimic.CHARTEVENTS
    note = mimic.NOTEEVENTS
    micro = mimic.MICROBIOLOGYEVENTS

    docs = {}
    titles = ['GENDER']
    docs = doc_gen(docs, patients, titles)

    titles = ['MARITAL_STATUS', 'ETHNICITY', 'DIAGNOSIS']
    docs = doc_gen(docs, admit, titles)

    titles = ['ITEMID', 'VALUE']
    docs = doc_gen(docs, oute, titles, 'VALUE')

    titles = ['ITEMID', 'VALUE']
    docs = doc_gen(docs, labe, titles, 'VALUENUM')

    titles = ['ITEMID', 'VALUE']
    docs = doc_gen(docs, charte, titles, 'VALUENUM')

    for item in micro.find({'SUBJECT_ID':patient_id}):
        docs[patient_id] = docs[patient_id] + ' ' + get_word(item['SPEC_ITEMID'], item['INTERPRETATION'])

    for item in note.find({'SUBJECT_ID':patient_id}):
        text = ' '.join(re.findall(r'[a-zA-Z]+', item['TEXT']))
        docs[patient_id] = docs[patient_id] + ' ' + text

    docs[patient_id] = docs[patient_id].replace(' ', '\t')

    p_docs = conn.diagnosis.patient_docs_test
    for u in docs:
        p_docs.insert_one({'SUBJECT_ID':u, 'time':datetime.now(), 'document':docs[u]})

    return True

def main():
    '''医生添加病人时，读取病人数据，形成文档'''

    print new_pdoc('92625')
    

if __name__ == '__main__':
    main()
