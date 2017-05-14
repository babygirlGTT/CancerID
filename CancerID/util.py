# -*- coding: utf-8 -*-  
"""
cancerID.utils
------------------
Helper functions used throughout CancerID.
"""
from sklearn.feature_extraction.text import CountVectorizer
import pymongo
from pymongo import MongoClient
import lda
import fire

class Database(object):

    def __init__(self):
        self.db_client = MongoClient()

    def get_doctor_info(self, doctor_id):
        doctor_db = self.db_client.get_database("doctor")
        coll = doctor_db.get_collection("doctorinfo")
        return coll.find_one({"id":doctor_id})

class Knowledgebase(object):

    def __init__(self):
        self.db_client = MongoClient()

    def get_knowledge(self):
        knowledge_db = self.db_client.get_database("knowledge")
        return knowledge_db

    def get_features(self, disease_id):
        'the type of disease is a string'
        db = self.get_knowledge()
        coll = db.get_collection(disease_id)
        latest_record = coll.find_one({}).sort("_id", pymongo.DESCENDING).limit(1)
        return latest_record['items']

def extract_data(patient_id = "all"):
    #mongodb中抽取数据形成文档存储
    client = MongoClient()
    coll = client.diagnosis.documents
    if patient_id == "all":
        docs = coll.find({})
    else:
        docs = coll.find({"p_id":patient_id}).sort([("_id",-1)]).limit(1)

    result = []
    for doc in docs:
        result.append(doc["doc"])

    return result 

def vectorize(docs):
    print("Extracting tf features for LDA...")
    # tf_vectorizer = CountVectorizer(max_df=1, min_df=1,stop_words='english')
    tf_vectorizer = CountVectorizer(stop_words='english')
    tf = tf_vectorizer.fit_transform(docs)
    tf_feature_names = tf_vectorizer.get_feature_names()
    return tf,tf_feature_names

def fitting(vecs):
    X = vecs.toarray()
    model = lda.LDA(n_topics=20, n_iter=1500, random_state=1)
    model.fit(X)  # model.fit_transform(X) is also available
    topic_word = model.topic_word_  # model.components_ also works
    return model

def main():
    docs =  extract_data("all")
    vecs,names = vectorize(docs)
    model = fitting(vecs)

if __name__ == "__main__":
    main()