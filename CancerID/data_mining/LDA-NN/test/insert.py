# -*- coding: utf-8 -*-  
import pymongo
from pymongo import MongoClient
from datetime import datetime
#如果没有数据 跑这个程序
import numpy as np
import pandas as pd
import json

diagnose_result = np.load('../result/simple_result.npy')

with open('../data/dis_dic.json','rb') as f:
    dic = json.load(f)

numbers = [36, 80, 145, 200, 266, 300, 385, 446, 591, 788, 883, 1112]

p_real = {36:'71262', 80:'84972', 145:'90391', 200:'80158', 266:'69448', 300:'77644', 385:'79418', 446:'88971', 591:'84837', 788:'99141', 883:'92625', 1112:'69498'}
client = MongoClient()
for i in numbers:
    diagnose_fil =np.argsort(diagnose_result[i,:])[::-1]
    prob = diagnose_result[i,:][diagnose_fil]
    icd = [] 
    for item in diagnose_fil:
        for icdcode, value in dic.items():
            if item == value:
                icd.append(icdcode)
    diagnose =  [{"icd_9":str(icd[j]),'prob':round(prob[j],5)*100} for j in range(416)]
    diagnose_insert = {
            "p_id":p_real[i],
            "diagnose":diagnose,
            "diagnose_time":datetime.now()
        }
    client.diagnosis.results.insert_one(diagnose_insert)