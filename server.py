# -*- coding: utf-8 -*-
''' server '''

import os
import datetime
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import json
from tornado import gen
import pymongo
from pymongo import MongoClient
from tornado.options import define, options

define("port", default=8080, help="run on the given port", type=int)
# executor = concurrent.futures.ThreadPoolExecutor(2)
class BaseHandler(tornado.web.RequestHandler):
    '''Base Handler'''
    @property #属性
    def db_client(self):
        return self.application.db_client

    def get_current_user(self):
        user_id = self.get_secure_cookie("doctor_id")
        if not user_id: return None #没有此用户
        return self.db_client.doctor.doctorinfo.find_one({"id":user_id})

class MainHandler(BaseHandler):

    def get_patient_info(self, patient_ids):
        '''病人简要信息'''
        items = []
        for patient_id in patient_ids:
            info = self.db_client.patients.patient_info.find_one({"p_id":patient_id})
            items.append(info)
        return items


    @tornado.web.authenticated
    def get(self):
        # name = tornado.escape.xhtml_escape(self.current_user)
        # self.write("Hello, " + name)
        user = self.get_current_user()
        patients = self.get_patient_info(user["patients"])
        self.render("Modules/index.html", user=user, patients=patients)

class LoginHandler(BaseHandler):
    def get(self):
        self.render("Modules/login.html", error=None)

    @gen.coroutine #异步
    def post(self):
        doctor = self.db_client.doctor.doctorinfo.find_one({"id":self.get_argument("doctor_id")})
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
        self.redirect(self.get_argument("next","/"))

class DiagHandler(BaseHandler):
    def get_patient_info(self, patient_id):
        '''病人简要信息'''
        items = self.db_client.patients.patient_info.find_one({"p_id":patient_id})
        return items

    def get_diag_results(self, patient_id):
        '''诊断结果'''
        items = self.db_client.diagnosis.results.find_one({"p_id":patient_id})
        d_name = self.db_client.d_icd9.results.find_one({"p_id":patient_id})
        items['diagnose'].sort(key=lambda x: x["prob"])
        items['diagnose'].reverse() #倒序
        return items['diagnose']
    # def get_diag_evidence(self, patient_id):
    #     '''诊断依据'''
    #     pass

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
        # self.render("Modules/test.html", user=user, recommend=recommend, diag=diag, info=info)
        self.render("Modules/diagnosis.html", user=user, diag=diag, info=info)

    def post(self):
        p_id = self.get_argument("p_id")        
        link = "/records/"+p_id
        self.redirect(self.get_argument("next",link))

class RecordsHandler(BaseHandler):
    def get(self, input):
        p_id = input
        print p_id
        self.render("Modules/hello.html")

class HelloModule(tornado.web.UIModule):
    def render(self):
        return '<h1>Hello, world!</h1>'

class Application(tornado.web.Application):
    '''define application'''
    def __init__(self):
        handlers = [(r"/", MainHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    (r"/diagnosis/(\w+)", DiagHandler),
                    (r"/records/(\w+)", RecordsHandler),
                    ]

        settings = dict(
            title=u"CancerID-CodePlay",
            cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            ui_modules={'Hello': HelloModule},
            login_url="/login",#重定向路径
            xsrf_cookies=True,
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
