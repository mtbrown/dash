import sys
import os

plugins_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "plugins"))  # ../plugins
_plugins = {}


def load_plugins():
    sys.path.insert(0, plugins_path)
    for f in os.listdir(plugins_path):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            mod = __import__(fname)
            _plugins[fname] = mod.main
    sys.path.pop(0)
