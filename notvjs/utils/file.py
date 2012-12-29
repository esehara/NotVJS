import os


class FileManager:

    ROOT = os.path.join(
        os.path.join(os.path.normpath(
            os.path.dirname(__file__)), '..'),
        '..')

    static_path = os.path.join(
        ROOT, 'static')

    filelist = os.listdir(
        os.path.join(static_path, 'pic'))

    def __init__(self):
        self.tempfile = None
        self.pointer = 0

    def current(self):
        if self.tempfile is None:
            return "pic/" + self.filelist[self.pointer]
        else:
            return self.tempfile

    def next(self):
        self.tempfile = None
        self.pointer += 1
        if self.pointer >= len(self.filelist):
            self.pointer = 0
        return self.current()

    def past(self):
        self.tempfile = None
        self.pointer -= 1
        if self.pointer < 0:
            self.pointer = len(self.filelist) - 1
        return self.current()

    def set_path(self, path):
        self.tempfile = path
