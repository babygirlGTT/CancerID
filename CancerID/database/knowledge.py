# -*- coding: utf-8 -*-  

from pymongo import MongoClient

class Knowledgebase(object):
    '''Knowledgebase'''

    def __init__(self):
        self.db = MongoClient('localhost', 27017).diagnosis

    def get_diag_result(self, disease_id):
        coll = self.db.knowledge 
        return coll.find_one({'p_id':patient_id})

    def get_1(self):
        return client.doctor

    def get_2(self):
        return client.doctor
