# coding:utf-8

from datetime import datetime
import numpy as np
import re

from pymongo import MongoClient


def new_ptf(patient_id):
    '''根据病人文档，生成病人词频矩阵'''

    conn = MongoClient('118.89.186.110', 27017)
    p_doc = conn.diagnosis.patient_docs_test
    p_tf = conn.patients.patient_tf_test

    doc = [item for item in p_doc.find({'SUBJECT_ID':patient_id})][-1]['document']
    doc_ls = doc.lower().split()
    with open('/home/zn/Desktop/data/matrix/lda/wordls.txt', 'r') as f:
        wordls = [word.strip() for word in f.readlines()]

    # 将病人文档生成 '词：词频' 字典
    word_dic = dict()
    for word in doc_ls:
        if word in word_dic:
            word_dic[word] = word_dic[word] + 1
        else:
            word_dic[word] = 1
    # print word_dic

    # 生成词频矩阵
    tf = []
    for word in wordls:
        if word in word_dic:
            tf.append(word_dic[word])
        else:
            tf.append(0)
    # print np.array(tf).sum()

    # 插入patient_tf表中
    p_tf.insert_one({'SUBJECT_ID':patient_id, 'tf':tf, 'isTrue':1, 'check':0, 'time':datetime.now()})

    item_ls = []
    for item in conn.knowledge.disease_knowledge.find():
        item_ls += item['ITEMS'].split()
    # print item_ls

    tf = []
    for word in wordls:
        if word in word_dic:
            item_id = re.findall(r'\d+_', word)
            if item_id:
                if item_id[0][:-1] not in item_ls:
                    tf.append(word_dic[word])
                else:
                    print item_id[0][:-1]
                    tf.append(0)
            else:
                tf.append(word_dic[word])
        else:
            tf.append(0)
    # print tf
    # print np.array(tf).sum()

    p_tf.insert_one({'SUBJECT_ID':patient_id, 'tf':tf, 'isTrue':0, 'check':0, 'time':datetime.now()})

def main():
    '''main()'''

    new_ptf('96115')

if __name__ == '__main__':
    main()
