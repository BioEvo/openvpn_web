from tornado.web import RequestHandler

import os
import sys
import base64
import logging
from tornado.log import LogFormatter


class BaseHandler(RequestHandler):
    def initialize(self):
        '''
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        datefmt = '%Y-%m-%d %H:%M:%S'
        fmt = '%(color)s[%(levelname)1.1s %(asctime)s]%(end_color)s %(message)s'
        formatter = LogFormatter(color=True, datefmt=datefmt, fmt=fmt)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logdir = os.path.join(self.settings['static_path'], "../logs")
        file_handler = logging.FileHandler(os.path.join(logdir, 'debug.log'))
        file_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        '''

    def prepare(self):
        if self.request.method == "POST":
            if sys.version_info.major == 2:
                self.request.body = base64.decodestring(self.request.body)
            if sys.version_info.major == 3:
                self.request.body = base64.decodebytes(self.request.body).decode()

    def write_error(self, status_code, **kwargs):
        self.finish("%(message)s" % {"message": kwargs['result']})

