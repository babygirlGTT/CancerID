import unittest
import diagnose_test
import numpy as np
import re
from pymongo import MongoClient

class Test(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient()

    #load_data
    def test_load_data(self):
        data = diagnose_test.load_data(self.client)
        self.assertTrue(data)

    #load_model
    def test_load_model(self):
        model = diagnose_test.load_dia_model(path='./CancerID/data_mining/LDA-NN/model/')
        self.assertTrue(model)

    #perform_exam
    def test_do_exam(self):
        wordls = ['a','b','c','d','e']
        raw_item = np.array([0,2,5,0,1])
        to_do = ['a','b','c']
        items = np.array([0,0,0,0,0]) 
        for i in range(len(items)):
            word = re.findall('^[a-z]+$',wordls[i])
            if word:
                if word[0] in to_do:
                    if items[i] == 0 and raw_item[i] > 0 :
                        items[i] = raw_item[i]
    for j in range(len(items)):
        self.assertEqual(items[j], np.array([0,2,5,0,0])[j])

    #diagnose
    def test_diagnose(self):
        p_data,p_id = diagnose_test.load_data(self.client)
        model = diagnose_test.load_dia_model(path='./CancerID/data_mining/LDA-NN/model/')
        patient_topic = diagnose_test.tf_to_topic(p_data)
        p_topics = model.predict(patient_topic)
        self.assertEqual(len(p_topics[0]),416)

if __name__ == '__main__':
    unittest.main()


