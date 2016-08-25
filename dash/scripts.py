import logging
import os
import sys
import threading
import time
import enum

from .grid import Grid
from .panel import Panel


class ScriptStatus(enum.Enum):
    Ok = "ok"
    Warning = "warning"
    Error = "error"


class Script:
    def __init__(self, id, main, grid):
        self.id = id  # name of module/package containing script
        self.title = id
        self.status = ScriptStatus.Ok
        self.label = 0
        self.main = main
        self.grid = grid
        self.panel = Panel(id, self.grid, [])
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
        for file in os.listdir(self.scripts_path):
            self.start_script(file)
        while not self._stop.is_set():
            self.verify_scripts()
            time.sleep(10)
        logging.info("ScriptManager is stopping")

    def start_script(self, filename):
        name, ext = os.path.splitext(filename)
        layout_file = os.path.join(self.scripts_path, name, 'layout.html')

        sys.path.insert(0, self.scripts_path)
        mod = __import__(name)
        sys.path.pop(0)

        if not hasattr(mod, "main"):
            return

        layout = open(layout_file).read()
        grid = Grid(layout)

        script = Script(name, mod.main, grid)
        self.script_list.append(script)
        self.script_map[script.id] = script

    def verify_scripts(self):
        logging.info("Checking status of script threads")
        for script in self.script_list:
            if not script.thread:
                logging.info("Creating new thread: {0}".format(script.id))
                script.thread = threading.Thread(target=script.main, args=(script.panel,))
            if not script.thread.is_alive():
                logging.info("Starting thread: {0}".format(script.id))
                script.thread.start()
