import abc
from ..api import socket


class Component:
    __metaclass__ = abc.ABCMeta

    def __init__(self, id: str, title: str = None):
        self.title = title
        self.containers = []  # grids that panel is currently contained in
        self.id = id

    @abc.abstractproperty
    def state(self):
        return {}

    def emit_state(self):
        socket.emit(self.id, self.state, namespace='/api', room=self.id)
