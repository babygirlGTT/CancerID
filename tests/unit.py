import unittest
from pymongo import MongoClient

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient()
    #zaccount
    def test_passwd(self):
        doctor = self.client.doctor.doctorinfo.find_one({"id":'10001'})
        self.assertEqual(doctor['passwd'], '666666')
    #patient_information
    def test_patient_info(self):
        info = self.client.patients.patient_info.find_one({})
        self.assertTrue(info)
    #disease discription
    def test_disease_list(self):
        dis_cription = self.client.diagnosis.d_icd.find_one({})
        self.assertTrue(dis_cription)
    #items_discription
    def test_items_disctiption(self):
        item_d = self.client.diagnosis.d_items.find_one({})
        self.assertTrue(item_d)
    #diagnosis_resut:
    def test_diagnosis_result(self):
        recommend = self.client.diagnosis.recommend.find({})
        self.assertTrue(recommend)
    #recommend(self):
    def test_recommend(self):
        result = self.client.diagnosis.results.find({})
        self.assertTrue(result)
    #records(self):
    def test_records(self):
        records = self.client.mimic.NOTEEVENTS.find({})
        self.assertTrue(records)

if __name__ == '__main__':
    unittest.main()


