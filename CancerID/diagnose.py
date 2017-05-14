# -*- coding: utf-8 -*-  
import pymongo
import fire
from pymongo import MongoClient
from sklearn import 
"""diagnose, from a document to a result."""

def load_data():
    #mongodb中抽取数据形成文档存储
    client = MongoClient()
    coll = client.diagnosis
    return coll.find()


dis = ["0001","0002","0003","0004","0005","0006"]

def load_model(path):
    pass
    return y

def predict(self, dis_list):

    prob = 1.0/len(dis_list) 
    result = [{disease:prob}for disease in dis_list]
    return result

def save_results(result):
    client = MongoClient()
    coll = client.diagnosis.results
    coll.insert({result})   

def main():
    # extract
    doc = extract_data('7001')["doc"]
    # tf idf
    pass
    # slda


if __name__ == "__main__": 
    fire.Fire()
    # main()