import inspect
import os
import importlib.util
from typing import Optional

from .grid import Grid
from . import context


class Script:
    def __init__(self, id):
        context.current_script = self
        self.id = id
        pass

    def render(self):
        return Grid()


def load_app_from_module(name: str, module_path: str) -> Optional[Script]:
    """
    Imports and inspects the Python module at the specified path. If a subclass
    of the App class is discovered, it is instantiated and returned. If no subclasses
    of the App class are found, None is returned.
    :param name: The name of the module used for __name__ when imported.
    :param module_path: Absolute path of python file to inspect.
    :return: An instance of App, or None
    """
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name, cls in inspect.getmembers(module, inspect.isclass):
        if issubclass(cls, Script):
            return cls()
    return None


def load_app(path: str) -> Optional[Script]:
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                name = os.path.splitext(file)[0]
                app = load_app_from_module(name, os.path.join(root, file))
                if app is not None:
                    return app
    return None
