import logging
import os
import sys
import threading
import time

from flask import render_template

from . import app
from .grid import Grid

plugins_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "plugins"))  # ../plugins
_plugins = []


class Plugin:
    def __init__(self, name, main):
        self.name = name
        self.main = main
        self.grid = Grid(name)
        self.thread = None


def load_plugins():
    sys.path.insert(0, plugins_path)
    for file in os.listdir(plugins_path):
        name, ext = os.path.splitext(file)
        mod = __import__(name)
        if hasattr(mod, "main"):
            setup_plugin(name, mod.main)
    sys.path.pop(0)


def setup_plugin(fname, main):
    new = Plugin(fname, main)
    _plugins.append(new)
    new.home_view = lambda: render_template('plugin/home.html', name=new.name, grid=new.grid)
    app.add_url_rule("/{0}".format(new.name), new.name, new.home_view)
    new.log_view = lambda: render_template('plugin/log.html', name=new.name, grid=new.grid)
    app.add_url_rule("/{0}/log".format(new.name), "{0}_log".format(new.name), new.log_view)


class PluginScheduler(threading.Thread):
    def __init__(self):
        super(PluginScheduler, self).__init__()
        self._stop = threading.Event()
        self.daemon = True  # stop scheduler and all plugins when main thread exits

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self):
        while not self._stop.is_set():
            logging.info("Checking status of plugin threads")
            for plugin in _plugins:
                if not plugin.thread:
                    logging.info("Creating new thread: {0}".format(plugin.name))
                    plugin.thread = plugin.thread = threading.Thread(target=plugin.main, args=(plugin.grid, ))
                if not plugin.thread.is_alive():
                    logging.info("Starting thread: {0}".format(plugin.name))
                    plugin.thread.start()
            time.sleep(10)
        logging.info("PluginScheduler is stopping")


def start_plugins():
    logging.info("Starting PluginScheduler")
    thread = PluginScheduler()
    thread.start()


def list_plugins():
    return _plugins
