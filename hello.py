import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import datetime
import pymongo
from pymongo import MongoClient
from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers=[(r"/(\w+)", NameHandler)]
        client = MongoClient('localhost',27017)
        self.db = client.doctor
    	tornado.web.Application.__init__(self, handlers, debug=True)
class NameHandler(tornado.web.RequestHandler):
    def get(self, name):
        coll = self.application.db.doctorinfo
        note = coll.find_one({"name": name})
        if note:
            del note["_id`"]
            self.write(note)
        else:
            self.set_status(404)
            self.write({"error":"no one"})

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
