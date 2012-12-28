# -*- coding: utf-8 -*-

import os
from utils import ImageDestory

class FileManager:

    ROOT = os.path.normpath(
        os.path.dirname(__file__))

    static_path = os.path.join(
        ROOT, 'static')
    
    filelist = os.listdir(
        os.path.join(static_path, 'pic'))

    def __init__(self):
        self.pointer = 0

    def current(self):
        return self.filelist[self.pointer]

    def next(self):
        self.pointer += 1
        if self.pointer >= len(self.filelist):
            self.pointer = 0
        return self.current()

    def past(self):
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = len(self.filelist) - 1
        return self.current()


class Binding:

    filemanager = FileManager()

    def __init__(self):
        self.bindings_key = {
            "PreviousPictureShow": self.previous_pic,
            "NextPictureShow": self.next_pic,
            "DestoryPicture": self.destory_pic}

        self.bindings = {
            "LoadPicture": self.set_picture,
                }

    def run_key_event(self, socket, event, *args, **kwargs):
        self.bindings_key[event](socket, *args, **kwargs)

    def run_event(self, socket, event, *args, **kwargs):
        self.bindings[event](socket, *args, **kwargs)

    def destory_pic(self, socket):
        picture_path = self.filemanager.current()
        img = ImageDestory("static/pic/" + picture_path)
        img.random_cut_paste()
        img.save('static/temp/destory.jpg')
        picture_path = 'temp/destory.jpg'
        self.set_picture(socket, picture_path)

    def previous_pic(self, socket):
        self.filemanager.past()
        self.set_picture(socket)

    def next_pic(self, socket):
        self.filemanager.next()
        self.set_picture(socket)

    def set_picture(self, socket, filename=None):

        if filename is None:
            filename = "/pic/" + self.filemanager.current()

        socket.broadcast(
            'set_image', filename)

    def test_print(self, socket):
        self.num += 1
        print self.num
