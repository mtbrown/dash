import sys
import os
import logging
import threading
import time
from flask import render_template

from . import components

plugins_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "plugins"))  # ../plugins
_plugins = []


class Plugin:
    def __init__(self, name, main):
        self.name = name
        self.main = main
        self.grid = components.Grid()
        self.thread = None
        self.view_func = lambda: render_template('plugin.html', name=self.name, panels=self.grid.panels)


def load_plugins():
    sys.path.insert(0, plugins_path)
    for f in os.listdir(plugins_path):
        fname, ext = os.path.splitext(f)
        if ext == '.py':
            mod = __import__(fname)
            _plugins.append(Plugin(fname, mod.main))
    sys.path.pop(0)


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
