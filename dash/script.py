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


def load_script_from_module(module_path: str) -> Optional[Script]:
    """
    Imports and inspects the Python module at the specified path. If a subclass
    of the Script class is discovered, it is instantiated and returned. If no subclasses
    of the Script class are found, None is returned.
    :param module_path: Absolute path of python file to inspect.
    :return: An instance of Script, or None
    """
    # name is the name of the module used for __name__ when imported
    name, ext = os.path.splitext(os.path.basename(module_path))
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for name, cls in inspect.getmembers(module, inspect.isclass):
        if issubclass(cls, Script):
            return cls()
    return None


def load_script(path: str) -> Optional[Script]:
    if not os.path.isdir(path):
        return load_script_from_module(path)

    for root, dirs, files in os.walk(path):
        for file in files:
            if not file.endswith('.py'):
                continue
            script = load_script_from_module(os.path.join(root, file))
            if script is not None:
                return script
    return None
