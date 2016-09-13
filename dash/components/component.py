import abc
from typing import Dict
from ..api import socket


class Component:
    __metaclass__ = abc.ABCMeta

    def __init__(self, id: str, title: str = None):
        self.title = title
        self.containers = []  # grids that panel is currently contained in
        self.id = id
        self._registered = []

    @abc.abstractproperty
    def state(self) -> Dict:
        """
        Returns a dictionary containing the current state of the component. This
        dictionary is sent to the client whenever a registered property is updated or
        emit_state() is called.
        """
        return {}

    def register_property(self, name, init):
        """
        Register a new property that is represents part of the current state of the component.
        After being registered, emit_state() will be called automatically whenever the property
        is set to a new value.
        Example usage: self.text = self.register_property('text', "")
        :param name: The name of the property
        :param init: The default value of the property
        :return: The default value of the property
        """
        self._registered.append(name)
        return init

    def __setattr__(self, name, value):
        self.__dict__[name] = value
        if hasattr(self, '_registered') and name in self._registered:
            self.emit_state()

    def emit_state(self):
        socket.emit(self.id, self.state, namespace='/api', room=self.id)
