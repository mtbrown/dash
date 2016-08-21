import logging
import os
import sys
import threading
import time
import enum

from .grid import Grid


class ScriptStatus(enum.Enum):
    Ok = "ok"
    Warning = "warning"
    Error = "error"


class Script:
    def __init__(self, id, main):
        self.id = id  # name of module/package containing script
        self.title = id
        self.status = ScriptStatus.Ok
        self.label = 0
        self.main = main
        self.grid = Grid(id)
        self.thread = None


class ScriptManager(threading.Thread):
    def __init__(self, scripts_path):
        super().__init__()
        self.scripts_path = scripts_path
        self._stop = threading.Event()
        self.daemon = True  # stop scheduler and all scripts when main thread exits
        self.script_list = []
        self.script_map = {}

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

    def run(self):
        self.load_scripts()
        while not self._stop.is_set():
            self.verify_scripts()
            time.sleep(10)
        logging.info("ScriptManager is stopping")

    def load_scripts(self):
        sys.path.insert(0, self.scripts_path)
        for file in os.listdir(self.scripts_path):
            name, ext = os.path.splitext(file)
            mod = __import__(name)
            if hasattr(mod, "main"):
                script = Script(name, mod.main)
                self.script_list.append(script)
                self.script_map[script.id] = script
        sys.path.pop(0)

    def verify_scripts(self):
        logging.info("Checking status of script threads")
        for script in self.script_list:
            if not script.thread:
                logging.info("Creating new thread: {0}".format(script.id))
                script.thread = threading.Thread(target=script.main, args=(script.grid,))
            if not script.thread.is_alive():
                logging.info("Starting thread: {0}".format(script.id))
                script.thread.start()
