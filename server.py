# -*- coding: utf-8 -*-
''' server '''

import os
from datetime import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado import gen
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import BSON
from tornado.options import define, options
from tornado.escape import json_decode

# import diagnose_test

define("port", default=80, help="run on the given port", type=int)


# executor = concurrent.futures.ThreadPoolExecutor(2)
class BaseHandler(tornado.web.RequestHandler):
    '''Base Handler'''

    @property  # 属性
    def db_client(self):
        return self.application.db_client

    def get_current_user(self):
        user_id = self.get_secure_cookie("doctor_id")
        if not user_id: return None  # 没有此用户
        return self.db_client.doctor.doctorinfo.find_one({"id": user_id})


class MainHandler(BaseHandler):
    def get_patient_info(self, patient_ids):
        '''病人简要信息'''
        items = []
        for patient_id in patient_ids:
            info = self.db_client.patients.patient_info.find_one({"p_id": patient_id})
            items.append(info)
        return items

    # 疾病icd9代码和文字描述
    def get_dis_text(self):
        dis_cription = self.db_client.diagnosis.d_icd.find_one()
        return dis_cription

    @tornado.web.authenticated
    def get(self):
        # name = tornado.escape.xhtml_escape(self.current_user)
        # self.write("Hello, " + name)
        user = self.get_current_user()
        patients = self.get_patient_info(user["patients"])

        disease_items = self.get_dis_text()
        self.render("Modules/index.html", disease_items=disease_items, user=user, patients=patients)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("Modules/login.html", error=None)

    @gen.coroutine  # 异步
    def post(self):
        doctor = self.db_client.doctor.doctorinfo.find_one({"id": self.get_argument("doctor_id")})
        if not doctor:
            self.render("Modules/login.html", error="没有找到此医生")
            return
        passwd = tornado.escape.utf8(self.get_argument("passwd"))
        if passwd == doctor['passwd']:
            self.set_secure_cookie("doctor_id", self.get_argument("doctor_id"))
            self.redirect(self.get_argument("next", '/'))
        else:
            self.render("Modules/login.html", error="密码不正确")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("doctor_id")
        self.redirect(self.get_argument("next", "/"))


class DiagHandler(BaseHandler):
    def get_patient_info(self, patient_id):
        '''病人简要信息'''
        items = self.db_client.patients.patient_info.find_one({"p_id": patient_id})
        return items

    def get_diag_results(self, patient_id):
        items = [result for result in self.db_client.diagnosis.results.find({"p_id": patient_id})][-1]
        d_name = self.db_client.d_icd9.results.find_one({"p_id": patient_id})
        items['diagnose'].sort(key=lambda x: x["prob"])
        items['diagnose'].reverse()  # 倒序
        return items['diagnose']

    def get_evi_topic(self):
        did_top = self.db_client.knowledge.dis_topics.find_one()
        return did_top

    def get_top_term(self):
        topic_term = self.db_client.knowledge.topic_words.find_one()
        return topic_term

    # 病人下疾病icd9代码的诊断推荐列表
    def get_recom_lists(self, patient_id):
        recommend_data = [item for item in self.db_client.diagnosis.recommend.find({"SUBJECT_ID": patient_id})][-1]
        return recommend_data['recommend']

    # 疾病icd9代码和文字描述
    def get_dis_text(self):
        dis_cription = self.db_client.diagnosis.d_icd.find_one()
        return dis_cription

    # 推荐检查项目代码和文字描述
    def get_items_text(self):
        items_cription = self.db_client.diagnosis.d_items.find_one()
        return items_cription

    # def get_recom_items(self, patient_id):
    #     '''推荐项目'''
    #     results = self.db_client.diagnosis.recommend.find_one({"p_id":patient_id})
    #     return results['items']
    @tornado.web.authenticated
    def get(self, input):
        user = self.get_current_user()
        # recommend = self.get_recom_items(input)
        diag = self.get_diag_results(input)
        info = self.get_patient_info(input)
        disease_evi = self.get_evi_topic()
        topic_term = self.get_top_term()
        reclists = self.get_recom_lists(input)
        disease_items = self.get_dis_text()
        items_detail = self.get_items_text()
        # self.render("Modules/test.html", user=user, recommend=recommend, diag=diag, info=info)
        self.render("Modules/newdiag.html", user=user, diag=diag, info=info, disease_evi=disease_evi,
                    topic_term=topic_term, reclists=reclists, disease_items=disease_items, items_detail=items_detail)

    # 接受POST请求
    def post(self):
        p_id = self.get_argument("p_id")
        link = "/records/" + p_id
        self.redirect(self.get_argument("next", link))


# 获取病历文本和检查单，病例单列表
class RecordsHandler(BaseHandler):
    def get(self, input):
        recordtxt = self.get_all_records(input)
        outputlist = self.get_all_outputs(input)
        info = self.get_patient_info(input)
        user = self.get_current_user()
        # uid = set()
        self.render("Modules/records.html", user=user, info=info, recordtxt=recordtxt, outputlist=outputlist)

    # 要写一个方法，读取好几个数据表，对得到的检查单id取并集，合并返回一个字典列表
    def get_all_outputs(self, patient_id):
        ckitems = self.db_client.mimic.CHARTEVENTS.find({"SUBJECT_ID": patient_id})
        output_ck = [item for item in ckitems]
        return output_ck

    def get_all_records(self, patient_id):
        sumtxts = self.db_client.mimic.NOTEEVENTS.find({"SUBJECT_ID": patient_id})
        sumtxt = [item for item in sumtxts]
        return sumtxt

    def get_patient_info(self, patient_id):
        '''病人简要信息'''
        items = self.db_client.patients.patient_info.find_one({"p_id": patient_id})
        return items


'''失败的ajax实验，给下面的UpdiagsHandler做参考
    def post(self,record_id):
        ckitem = self.get_argument("record_id")
        print type(ckitem)
        ckstr = str(ckitem)
        print type(ckstr)
        item_obj = BSON(ckstr)
        onerecord = self.db_client.mimic.OUTPUTEVENTS.find({"_id":ObjectId(ckstr)})
        result = [record for record in onerecord]
        #print ckitem
        print result
        return result
'''


# 处理前段提交的选中疾病指标的数据
class UpdiagsHandler(BaseHandler):
    def post(self, *args, **kwargs):
        # print self.request.body_arguments
        rawdata = self.request.body
        data = json.loads(rawdata)
        icd = data['diseasename']
        to_exam_list = data['newdata']
        p_id = data['p_id']
        to_insert = {
            'p_id': p_id,
            'to_exam': to_exam_list,
            'excuted': 0,
            'time': datetime.now()
        }
        self.db_client.diagnosis.exam.insert_one(to_insert)


class Application(tornado.web.Application):
    '''define application'''

    def __init__(self):
        handlers = [(r"/", MainHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/diagnosis/(\w+)", DiagHandler),
                    (r"/records/(\w+)", RecordsHandler),
                    (r"/updiags/testup", UpdiagsHandler),  # 处理前段提交的选中疾病指标的数据
                    ]

        settings = dict(
            title=u"CancerID-CodePlay",
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            login_url="/login",  # 重定向路径
            xsrf_cookies=True
        )
        self.db_client = MongoClient('118.89.186.110', 27017)
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    '''main function'''
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
