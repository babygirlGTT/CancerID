# -*- coding: utf-8 -*-  
import pymongo
from pymongo import MongoClient
#如果没有数据 跑这个程序
client = MongoClient()
dic = [{"id":'10001',
       "name":'姚望',
       "passwd":'666666',
       "patients":['7001','7002'] },
        {"id":'10002',
       "name":'吴林容',
       "passwd":'666666',
       "patients":['6001','6002','60003'] }
client.doctor.doctorinfo.insert_many(dic)