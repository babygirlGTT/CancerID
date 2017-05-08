# -*- coding: utf-8 -*-  
"""
cancerID.utils
------------------
Helper functions used throughout CancerID.
"""
from sklearn.feature_extraction.text import CountVectorizer
from pymongo import MongoClient
import lda
import fire
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