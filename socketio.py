# -*- coding: utf-8 -*-
from bind import Binding
from tornadio2 import SocketConnection, event

class EventConnection(SocketConnection):
    
    binding = Binding()
    participants = set()

    def on_open(self, info):
        self.participants.add(self)

    def on_close(self):
        self.participants.remove(self)

    def broadcast(self, event, message):
        for p in self.participants:
            p.emit(event, message)

    @event
    def EchoPicture(self, event):
        self.broadcast('set_image', event)

    @event
    def Event(self, event):
        print event
        self.binding.run_event(self, event)

    @event
    def KeyEvent(self, event):
        print event
        self.binding.run_key_event(self, event)
