import sys
import os
from flask import render_template

from . import components

plugins_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "plugins"))  # ../plugins
_plugins = []


class Plugin:
    def __init__(self, name, main):
        self.name = name
        self.main = main
        self.grid = components.Grid()
        self.view_func = lambda: render_template('base.html', name=self.name)


def load_plugins():
    sys.path.insert(0, plugins_path)
    for f in os.listdir(plugins_path):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            mod = __import__(fname)
            _plugins.append(Plugin(fname, mod.main))
    sys.path.pop(0)


def list_plugins():
    return _plugins
