# -*- coding: utf-8 -*-

from os import path
import json
import tornado.web
from socketio import EventConnection
from tornadio2 import TornadioRouter

ROOT = path.normpath(path.dirname(__file__))
static_path = path.join(ROOT, 'static/')

class NotVJSHandler:
    class Index(tornado.web.RequestHandler):
        def get(self):
            self.render('static/index.html')

    class Socket(tornado.web.RequestHandler):
        def get(self):
            self.render('static/socket.io.js')

    class ShortcutJS(tornado.web.RequestHandler):
        def get(self):
            self.render('static/shortcut.js')

EventRouter = TornadioRouter(
    EventConnection)


class Upload(tornado.web.RequestHandler):

    def post(self):

        response = {
            'status': False,
            'path': None}

        if not 'filearg' in self.request.files:
            return self.finish(
                json.dumps(response))

        fileinfo = self.request.files['filearg'][0]
        print "fileinfo is", fileinfo
        fname = fileinfo['filename']
        fh = open("static/pic/" + fname, 'w')
        fh.write(fileinfo['body'])

        response['status'] = True
        response['path'] = "pic/" + fname
        self.finish(
            json.dumps(response))

application = tornado.web.Application(
    EventRouter.apply_routes([
        (r"/", NotVJSHandler.Index),
        (r"/socket.io.js", NotVJSHandler.Socket),
        (r"/shortcut.js", NotVJSHandler.ShortcutJS),
        (r"/pic/(.*)", tornado.web.StaticFileHandler, {
            'path': path.join(static_path, "pic")}),
        (r"/temp/(.*)", tornado.web.StaticFileHandler, {
            'path': path.join(static_path, "temp")}),
        (r"/js/(.*)", tornado.web.StaticFileHandler, {
            'path': path.join(static_path, "js")}),
        (r"/css/(.*)", tornado.web.StaticFileHandler, {
            'path': path.join(static_path, "css")}),
        (r"/upload$", Upload)]),
    flash_policy_port=843,
    flash_policy_file=path.join(ROOT, 'flashpolicy.xml'),
    socket_io_port=8888)
