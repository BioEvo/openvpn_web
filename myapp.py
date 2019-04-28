import os
from tornado.web import Application, RedirectHandler
import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options

from handler.default import AdminHandler, LoginHandler
from handler.default import MainHandler, UserHandler
from handler.default import AddHandler, UpdateHandler, DelHandler
from handler.default import LogsHandler


define("port", default=8000, help="port to listen on")
curpath = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    setting = {
        "autoreload": True,
        "debug": False,
        "template_path": os.path.join(curpath, "templates"),
        "static_path": os.path.join(curpath, "static"),
        "xsrf_cookies": False,
    }
    app = Application([
        (r"/login", LoginHandler),
        (r"/", MainHandler),
        (r"/admin", AdminHandler),
        (r"/user", UserHandler),
        (r"/add", AddHandler),
        (r"/op", UpdateHandler),
        (r"/del", DelHandler),
        (r"/logs", LogsHandler),
    ], **setting)

    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
