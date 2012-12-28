# -*- coding:utf-8 -*-
import tornado.ioloop
import tornado.web

from tornado.web import asynchronous
from tornadio2 import SocketServer
from multiprocessing.pool import ThreadPool

from time import sleep
from route import application, NotVJSHandler


class MainHandler(tornado.web.RequestHandler):
    
    _workers = ThreadPool(10)

    @asynchronous
    def get(self):
        """
        rootにアクセスしたときに実行される
        """
        self.run_background(
            self.blocking_task, self.on_complete, (1, ))
    
    def blocking_task(self, n):
        """
        実際に実行される関数 
        """
        sleep(n)
        return n

    def run_background(self, func, callback, args=(), kwrds={}):
        """
        まず実行される関数
        """
        def _callback(result):
            """
            blocking taskが終了したあとに実行される関数
            """
            tornado.ioloop.IOLoop.instance().add_callback(
                lambda: callback(result))
        self._workers.apply_async(func, args, kwrds, _callback)

    def on_complete(self, res):
        self.write("Test %d </br>" % res)
        self.finish()

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    SocketServer(application)
