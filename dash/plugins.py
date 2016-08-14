import logging
import os
import sys
import threading
import time
import enum

from flask import render_template

from . import app
from .grid import Grid

plugins_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "plugins"))  # ../plugins
_plugins = []


class ScriptStatus(enum.Enum):
    Ok = "ok"
    Warning = "warning"
    Error = "error"


class Plugin:
    def __init__(self, id, main):
        self.id = id  # name of module/package containing script
        self.title = id
        self.status = ScriptStatus.Ok
        self.label = 0
        self.main = main
        self.grid = Grid(id)
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
    new.home_view = lambda: render_template('plugin/home.html', name=new.id, grid=new.grid)
    app.add_url_rule("/{0}".format(new.id), new.id, new.home_view)
    new.log_view = lambda: render_template('plugin/log.html', name=new.id, grid=new.grid)
    app.add_url_rule("/{0}/log".format(new.id), "{0}_log".format(new.id), new.log_view)


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
