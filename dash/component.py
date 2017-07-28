import abc
from typing import Dict

from .api import emit_component_state
from . import context


class Component:
    __metaclass__ = abc.ABCMeta

    def __init__(self, id: str):
        self.id = id
        self.script = context.current_script
        self._registered = {}


    @abc.abstractproperty
    def state(self) -> Dict:
        """
        Returns a dictionary containing the current state of the component. This
        dictionary is sent to the client whenever a registered property is updated or
        emit_state() is called.
        """
        return {}

    @property
    def grid_state(self):
        return {
            'type': self.__class__.__name__,
            'id': self.id
        }

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
        self._registered[name] = False  # False indicates the property hasn't been initialized
        return init

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if hasattr(self, '_registered') and name in self._registered:
            if self._registered[name]:  # check if property has been initialized
                self.emit_state()
            else:
                self._registered[name] = True  # mark property as initialized

    def emit_state(self):
        emit_component_state(self.script.id, self.id, self.state)
