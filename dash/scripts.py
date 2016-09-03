import os
import enum
from typing import List
import threading

from .grid import Grid, parse_layout
from .panel import Panel
from .hooks import ScriptHook, HookEvent, load_hooks
from .scheduler import ScheduledTask
from .components.component import Component


script_list = []

script_map = {}

script_path_map = {}


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
            self.hooks[hook.event].append(hook)


def load_scripts(path, scheduler):
    for name in os.listdir(path):
        script_path = os.path.join(path, name)
        layout_file = os.path.join(script_path, 'layout.html')

        hooks = load_hooks(script_path)
        if not hooks or script_path in script_path_map:
            continue  # skip directory/file if no hooks were found
        grid, component_list = parse_layout(open(layout_file).read())
        script = Script(name, grid, component_list, hooks)
        script_list.append(script)
        script_map[script.id] = script
        script_path_map[script_path] = script

        start_script(script, scheduler)


def start_script(script, scheduler):
    # Run setup hooks once
    for hook in script.hooks[HookEvent.Setup]:
        start_hook(script, hook)

    # Add scheduled tasks to the scheduler
    for hook in script.hooks[HookEvent.Schedule]:
        task = ScheduledTask(hook.schedule, callback=start_hook, args=[script, hook])
        scheduler.add_task(task)


def start_hook(script, hook):
    script.thread = threading.Thread(target=hook.callback, args=[script.panel])
    script.thread.start()


