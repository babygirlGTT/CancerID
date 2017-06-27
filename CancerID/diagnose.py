"""diagnose, from a document to a result."""

from pymongo import MongoClient
from keras.models import Sequential, load_model
from datetime import datetime
import numpy as np
import lda
import json
import re


def pre_process(self, parameter_list):
    pass


def load_data(client):
    coll = client.patients.patient_tf
    data = np.array([item['tf'] for item in coll.find({'check': 0})])
    id_list = [item['SUBJECT_ID'] for item in coll.find({'check': 0})]
    print(data.shape)
    print(id_list)
    return data, id_list


def load_dia_model(path):
    model = Sequential()
    model = load_model(path + 'simple.json')
    model.load_weights(path + "simple.h5")
    return model


def tf_to_topic(data):
    return transform(X=data)


def transform(X, max_iter=20, tol=1e-16):
    if isinstance(X, np.ndarray):
        # in case user passes a (non-sparse) array of shape (n_features,)
        # turn it into an array of shape (1, n_features)
        X = np.atleast_2d(X)
    doc_topic = np.empty((X.shape[0], 20))
    WS, DS = lda.utils.matrix_to_lists(X)
    for d in np.unique(DS):
        doc_topic[d] = _transform_single(WS[DS == d], max_iter, tol)
    return doc_topic


def _transform_single(doc, max_iter, tol):
    # load components for transform
    components = np.load("./data_mining/LDA-NN/data/components.npy")
    PZS = np.zeros((len(doc), 20))
    for iteration in range(max_iter + 1):  # +1 is for initialization
        PZS_new = components[:, doc].T
        PZS_new *= (PZS.sum(axis=0) - PZS + 0.01)
        PZS_new /= PZS_new.sum(axis=1)[:, np.newaxis]  # vector to single column matrix
        delta_naive = np.abs(PZS_new - PZS).sum()
        PZS = PZS_new
        if delta_naive < tol:
            break
    theta_doc = PZS.sum(axis=0) / PZS.sum()
    assert len(theta_doc) == 20
    assert theta_doc.shape == (20,)
    return theta_doc


def gen_recom_items(patient_id, patient_data_arr, client):
    wordls = client.knowledge.word_list.find_one({})['word_list']
    for i in range(patient_data_arr.shape[0]):
        items = []
        for j in range(len(patient_data_arr[i])):
            if patient_data_arr[i][j] == 1:
                word = re.findall(r'\d+_', wordls[j])
                if word:
                    items.append(word[0][:-1])
        examed_set = set(items)
        recommend = {}

        # knowledge
        knowledge = client.knowledge.disease_knowledge.find({})

        for item in knowledge:
            icd = item['ICD9_CODE']
            knowledge_set = set(item['ITEMS'].split())
            results = list(knowledge_set - examed_set)
            recommend[icd] = results
        client.diagnosis.recommend.insert_one({'SUBJECT_ID': patient_id[i], 'recommend': recommend})
        print
        i


def do_exams(patient_id, patient_data_arr, client):
    wordls = client.knowledge.word_list.find_one({})['word_list']
    exam = client.diagnosis.exam
    array = np.load('./data/test_df_s.npy')
    for i in range(len(patient_id)):

        to_do = [item for item in exam.find({'p_id': patient_id[i], 'excuted': 0})]
        if to_do:
            todo = to_do[-1]['to_exam']
        else:
            continue
        patient_tf = client.patients.patient_tf
        items = patient_data_arr[i]
        raw_item = array[i]

        for j in range(len(items)):
            word = re.findall(r'\d+_', wordls[j])
            if word:
                if word[0][:-1] in to_do:
                    print
                    'is todo'
                    print
                    word[0][:-1]
                    if items[i] == 0 and raw_item[i] > 0:
                        items[i] = raw_item[i]
                        print
                        i
                        # client.patients.patient_tf.insert_one({'SUBJECT_ID':patient_id[i], 'check':0, 'tf':list(items),'time':datetime.now()})
    exam.update_many({'excuted': 0}, {"$set": {'excuted': 1}})


def to_insert(patient_id, data, client):
    with open('./data/dis_dic.json', 'rb') as f:
        dic = json.load(f)
    results = []
    for i in range(data.shape[0]):
        diagnose_fil = np.argsort(data[i, :])[::-1]
        prob = data[i, :][diagnose_fil]
        icd = []
        for item in diagnose_fil:
            for icdcode, value in dic.items():
                if item == value:
                    icd.append(icdcode)
        diagnose = [{"icd_9": str(icd[j]), 'prob': round(prob[j], 5) * 100} for j in range(416)]
        diagnose_insert = {
            "p_id": patient_id[i],
            "diagnose": diagnose,
            "diagnose_time": datetime.now()
        }
        # print diagnose_insert
        client.diagnosis.results.insert_one(diagnose_insert)
        # print i
        results.append(diagnose[0]['icd_9'])
    return results


def update_patient_info(patient_id, results, client):
    for index, patient in enumerate(patient_id):
        item = client.patients.patient_info.find_one({'p_id': patient})
        print(item)
        item['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['result'] = results[index]
        print(item)
        client.patients.patient_info.update_one({'p_id': patient}, {'$set': item})


def main():
    # extract
    client = MongoClient()
    patient_data, patient_id = load_data(client)
    # patient_data = np.load('./data/test_df_s.npy')
    # patient_id = ['71262', '84972', '90391', '80158', '69448', '77644', '79418', '88971', '84837', '99141', '92625', '69498']
    # #load model
    model = load_dia_model(path="./data_mining/LDA-NN/model/")
    # # # dimension reducition
    patient_topic = tf_to_topic(patient_data)
    # # # prediction
    result = model.predict(patient_topic)
    # gen_recom_items(patient_id,patient_data, client)
    # do_exams(patient_id,patient_data, client)
    results = to_insert(patient_id, result, client)
    update_patient_info(patient_id, results, client)
    # coll = client.diagnosis.exam
    # coll.update_many({'check':0},{"$set":{'check':1}})


if __name__ == "__main__":
    main()