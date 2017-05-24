# -*- coding: utf-8 -*-  
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime, time, date
#如果没有数据 跑这个程序

client = MongoClient("localhost",port=27017)

dic = [{"id":'10001',
       "name":'姚望',
       "passwd":'666666',
       "patients":['7001','7002'] },
        {"id":'10002',
       "name":'吴林容',
       "passwd":'666666',
       "patients":['6001','6002','60003'] }]
diag_result = [{
    "p_id":'7001',
    "diagnose":[
        {"icd_9":"10029","prob":0.11},
        {"icd_9":"10030","prob":0.12},
        {"icd_9":"10031","prob":0.13},
        {"icd_9":"10032","prob":0.14},
    ],
    # "diagnose_time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    },
{
    "p_id":'7002',
    "diagnose":[
        {"icd_9":"10129","prob":0.13},
        {"icd_9":"10230","prob":0.14},
        {"icd_9":"10331","prob":0.15},
        {"icd_9":"10432","prob":0.16},
    ],
    # "diagnose_time":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
}]
documents = [{
    "p_id" : "7001",
    # "stored_time" : time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
    "stored_time" : datetime.now(),
    "doc" : "recorded as having No Known Allergies to Drugs Fatigue and Diarrhea Intubation 76 M with metastatic gastric CA on week 2 of palliative CIsplatin/CPT-11, presents with increasing weakness and diarrhea x5days. There have been no fevers, chills at home, no cough, dysuria, or other localizing symptoms besides the diarrhea. The pt's family called the oncologist who encouraged them to seek care in the ED.In the ED at 1115 [2777-1-28]: vitals were t98.1 p 108 bp 98/60 rr 22 98 5 on 5L. He was noted to be neutropenic with ANC<200. At 2:45 pm, pt was noted to have pulse 148 which was demonstrated on 12 lead to be a-fib. BP at this time was 95/52. His lactate went from 1.4 at 1pm to 4.3 at 4pm. He started on sepsis protocol and cnetral line was placed, he was aggressively volume resuscitated wtih 6.5 liters NS. The bp became progressively less stable and the pt was started on Neosynephrine. He was given cefepime and vanc. He was intubated in the ED in anticipation of possible cardioversion.Gastric CA. Diagnosed [3-25] after presenting with abdominal pain, melena, anemia, and weight loss. He was noted to have peritoneal carcinomatosis. He underwent chemo with epirubicin, cisplatin and 5-FU from [Month (only) 113] to [2776-9-21]. He recently started CIsplatin/CPT-11 [12-27]. 1) Nephrectomy in [2770] to remove RCC per daughter 2) ulcers 30 years ago Mandarin/Japanese speaking man who grew up in northeast mainland [Country ]. Married, lives with his wife.  Quit smoking and alcohol 5 years ago post nephrectomy.  Denied a history of heavy alcohol intake in the past."
},{
    "p_id" : "7001",
    # "stored_time" : time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
    "stored_time" : datetime.now(),
    "doc" : "Patient recorded as having No Known Allergies to Drugs Fatigue and Diarrhea Intubation 76 M with metastatic gastric CA on week 2 of palliative CIsplatin/CPT-11, presents with increasing weakness and diarrhea x5days. There have been no fevers, chills at home, no cough, dysuria, or other localizing symptoms besides the diarrhea. The pt's family called the oncologist who encouraged them to seek care in the ED.In the ED at 1115 [2777-1-28]: vitals were t98.1 p 108 bp 98/60 rr 22 98 5 on 5L. He was noted to be neutropenic with ANC<200. At 2:45 pm, pt was noted to have pulse 148 which was demonstrated on 12 lead to be a-fib. BP at this time was 95/52. His lactate went from 1.4 at 1pm to 4.3 at 4pm. He started on sepsis protocol and cnetral line was placed, he was aggressively volume resuscitated wtih 6.5 liters NS. The bp became progressively less stable and the pt was started on Neosynephrine. He was given cefepime and vanc. He was intubated in the ED in anticipation of possible cardioversion.Gastric CA. Diagnosed [3-25] after presenting with abdominal pain, melena, anemia, and weight loss. He was noted to have peritoneal carcinomatosis. He underwent chemo with epirubicin, cisplatin and 5-FU from [Month (only) 113] to [2776-9-21]. He recently started CIsplatin/CPT-11 [12-27]. 1) Nephrectomy in [2770] to remove RCC per daughter 2) ulcers 30 years ago Mandarin/Japanese speaking man who grew up in northeast mainland [Country ]. Married, lives with his wife.  Quit smoking and alcohol 5 years ago post nephrectomy.  Denied a history of heavy alcohol intake in the past."
}]
knowledge = {
        "items":set(["300","301"]),
        "stored_time":datetime.now()
    }

# client.doctor.doctorinfo.insert_many(dic)
# client.diagnosis.results.insert_many(diag_result)
# client.diagnosis.documents.insert_many(documents)

client.knowledge.icd9_1000.insert_one(knowledge)