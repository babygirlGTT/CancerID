# -*- coding: utf-8 -*-  

from pymongo import MongoClient

class Database(object):
    '''Database'''

    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def connect_diagnosis(self):
        return self.client.diagnosis
    def connect_doctor(self):
        return self.client.doctor

    def get_diag_result(self,patient_id):
        coll = self.client.diagnosis.results 
        return coll.find_one({'p_id':patient_id})

    def get_1(self):
        return client.doctor

    def get_2(self):
        return client.doctor