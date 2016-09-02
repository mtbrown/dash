import os
import enum
from typing import List

from .grid import Grid, parse_layout
from .panel import Panel
from .hooks import ScriptHook, HookEvent, load_hooks
from .components.component import Component


script_list = []

script_map = {}


class ScriptStatus(enum.Enum):
    Ok = "ok"
    Warning = "warning"
    Error = "error"


class Script:
    def __init__(self, id: str, grid: Grid, component_list: List[Component], hooks: List[ScriptHook]):
        self.id = id  # name of module/package containing script
        self.grid = grid
        self.components = {comp.id: comp for comp in component_list}

        self.title = id  # title displayed
        self.status = ScriptStatus.Ok
        self.label = 0
        self.panel = Panel(self.id, self.grid, self.components)
        self.thread = None

        self.hooks = {event: [] for event in HookEvent}
        for hook in hooks:
            self.hooks[hook.event].append(hook.callback)


def load_scripts(path):
    for name in os.listdir(path):
        script_path = os.path.join(path, name)
        layout_file = os.path.join(script_path, 'layout.html')

        hooks = load_hooks(script_path)
        if not hooks:
            continue  # skip directory/file if no hooks were found
        grid, component_list = parse_layout(open(layout_file).read())
        script = Script(name, grid, component_list, hooks)
        script_list.append(script)
        script_map[script.id] = script
