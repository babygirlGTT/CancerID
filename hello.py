# -*- coding: utf-8 -*- 
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
import os
import pymongo
from pymongo import MongoClient
from tornado.options import define, options
define("port", default=8080, help="run on the given port", type=int)
# executor = concurrent.futures.ThreadPoolExecutor(2)

class BaseHandler(tornado.web.RequestHandler):
    @property #属性
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("doctor_id")
        if not user_id: return None #没有此用户
        return self.db.doctorinfo.find_one({"id":user_id})

class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        # name = tornado.escape.xhtml_escape(self.current_user)
        # self.write("Hello, " + name)
        name = self.get_current_user()["name"]
        patients = self.get_current_user()["patients"]
        self.render("Modules/mainbase.html",name=name,number = len(patients))


class LoginHandler(BaseHandler):
    def get(self):
        self.render("Modules/login.html", error=None)

    @gen.coroutine #异步
    def post(self):
        doctor = self.db.doctorinfo.find_one({"id":self.get_argument("doctor_id")})
        if not doctor:
            self.render("Modules/login.html", error="没有找到此医生")
            return
        passwd = tornado.escape.utf8(self.get_argument("passwd"))
        if passwd == doctor['passwd']:
            self.set_secure_cookie("doctor_id", self.get_argument("doctor_id"))
            self.redirect(self.get_argument("next",'/'))
        else: 
            self.render("Modules/login.html", error="密码不正确")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("doctor_id")
        self.redirect(self.get_argument("next","/"))

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[  
                    (r"/", MainHandler),
                    (r"/login", LoginHandler),
                    (r"/logout", LogoutHandler),
                    ]
        settings = dict(
            title = u"CancerID-CodePlay",
            cookie_secret = "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path = os.path.join(os.path.dirname(__file__), "template"),
            static_path = os.path.join(os.path.dirname(__file__),'static'),
            login_url = "/login",#重定向路径
            xsrf_cookies = True,
        ) 

        self.db = MongoClient('localhost',27017).doctor
    	tornado.web.Application.__init__(self, handlers, **settings)

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
