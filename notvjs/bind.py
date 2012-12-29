# -*- coding: utf-8 -*-

import os
from utils.file import FileManager
from utils.image import ImageDestory


class Binding:

    filemanager = FileManager()

    def __init__(self):
        self.bindings_key = {
            "PreviousPictureShow": self.previous_pic,
            "NextPictureShow": self.next_pic,
            "DestoryPicture": self.destory_pic,
            "SetBackground": self.set_background,
            "ClearBackground": self.clear_background,
            "RotatePicture": self.rotate_pic,
            "ColorLinePicture": self.colorline_pic,
            "ShadowLinePicture": self.shadowline_pic,
            "UpPicture": self.up_pic,
            "DownPicture": self.down_pic,
            "LeftPicture": self.left_pic,
            "RightPicture": self.right_pic,
            "ShowPictureToggle": self.show_picture_toggle}

        self.show_status = True
        self.picture_y = 0
        self.picture_x = 0
        self.current_background = None

        self.bindings = {
            "LoadConfigure": self.get_configure}

    def run_key_event(self, socket, event, *args, **kwargs):
        self.bindings_key[event](socket, *args, **kwargs)

    def run_event(self, socket, event, *args, **kwargs):
        self.bindings[event](socket, *args, **kwargs)

    def __set_tempfile(self, socket, picture_path):
        picture_path = 'temp/destory.jpg'
        self.filemanager.tempfile = picture_path
        self.set_picture(socket)

    def rotate_pic(self, socket):
        picture_path = self.filemanager.current()
        img = ImageDestory("static/" + picture_path)
        img.random_rotate()
        img.save('static/temp/destory.jpg')
        self.__set_tempfile(socket, picture_path)

    def colorline_pic(self, socket):
        picture_path = self.filemanager.current()
        img = ImageDestory("static/" + picture_path)
        img.random_draw_line_noise()
        img.save('static/temp/destory.jpg')
        self.__set_tempfile(socket, picture_path)

    def shadowline_pic(self, socket):
        picture_path = self.filemanager.current()
        img = ImageDestory("static/" + picture_path)
        img.random_shadow_line()
        img.save('static/temp/destory.jpg')
        self.__set_tempfile(socket, picture_path)

    def destory_pic(self, socket):
        picture_path = self.filemanager.current()
        img = ImageDestory("static/" + picture_path)
        img.random_cut_paste()
        img.save('static/temp/destory.jpg')
        self.__set_tempfile(socket, picture_path)

    def previous_pic(self, socket):
        self.filemanager.past()
        self.set_picture(socket)

    def next_pic(self, socket):
        self.filemanager.next()
        self.set_picture(socket)

    def clear_background(self, socket):
        self.current_background = None
        socket.broadcast(
            'set_background_image', '')

    def up_pic(self, socket):
        self.picture_y -= 50
        self.set_picture_position(socket)

    def down_pic(self, socket):
        self.picture_y += 50
        self.set_picture_position(socket)

    def left_pic(self, socket):
        self.picture_x -= 50
        self.set_picture_position(socket)

    def right_pic(self, socket):
        self.picture_x += 50
        self.set_picture_position(socket)

    def set_picture_position(self, socket):
        socket.broadcast(
            'set_position', {
                'x': self.picture_x,
                'y': self.picture_y})

    def set_background(self, socket):

        filename = self.filemanager.current()
        self.current_background = filename
        socket.broadcast(
            'set_background_image', filename)

    def get_configure(self, socket):

        get_configure = {
            'image': self.filemanager.current(),
            'background': self.current_background,
            'position': {
                'x': self.picture_x, 'y': self.picture_y},
            'show_status': self.show_status}

        socket.broadcast(
            'set_configure', get_configure)

    def set_picture(self, socket):

        filename = self.filemanager.current()
        socket.broadcast(
            'set_image', filename)
        self.filemanager.filelist = os.listdir(
            os.path.join(self.filemanager.static_path, 'pic'))

    def show_picture_toggle(self, socket):

        self.show_status = not self.show_status
        socket.broadcast(
            'show_image_toggle', self.show_status)

    def test_print(self, socket):
        self.num += 1
        print self.num
