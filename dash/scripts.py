import logging
import os
import sys
import threading
import time
import enum
from bs4 import BeautifulSoup
import inspect
import pkgutil
from types import ModuleType
from typing import List

from .grid import create_grid
from .panel import Panel
from .hooks import HookEvent, ScriptHook


class ScriptStatus(enum.Enum):
    Ok = "ok"
    Warning = "warning"
    Error = "error"


class Script:
    def __init__(self, id, grid, component_list, hooks):
        self.id = id  # name of module/package containing script
        self.grid = grid
        self.components = {comp.id: comp for comp in component_list}

        self.title = id  # title displayed
        self.status = ScriptStatus.Ok
        self.label = 0
        self.panel = Panel(self.id, self.grid, self.components)
        self.thread = None
        self.hooks = {event: [] for event in HookEvent}


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
            time.sleep(10)
        logging.info("ScriptManager is stopping")

    def load_scripts(self):
        for name in os.listdir(self.scripts_path):
            script_path = os.path.join(self.scripts_path, name)
            layout_file = os.path.join(script_path, 'layout.html')
            hooks = []
            for importer, modname, ispkg in pkgutil.walk_packages(path=[script_path], onerror=lambda x: None):
                module = importer.find_module(modname).load_module(modname)
                hooks.extend((load_hooks(module)))
            if hooks:
                grid, component_list = create_grid(layout_file)
                script = Script(name, grid, component_list, hooks)
                self.script_list.append(script)
                self.script_map[script.id] = script


def load_hooks(module: ModuleType) -> List[ScriptHook]:
    hooks = []
    for name, member in inspect.getmembers(module):
        if isinstance(member, ScriptHook):
            hooks.append(member)
    return hooks
