import enum
import os
import queue
import threading
from typing import List

from dash.component import Component
from .grid import Grid
from .hooks import ScriptHook, HookEvent, load_hooks
from .panel import Panel
from .scheduler import ScheduledTask

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

        self.title = id  # title displayed
        self.status = ScriptStatus.Ok
        self.label = 0

        self.components = {comp.id: comp for comp in component_list}
        for component in component_list:
            component.attach_to_script(self)

        self.hooks = {event: [] for event in HookEvent}
        for hook in hooks:
            self.hooks[hook.event].append(hook)

        self.panel = Panel(self.id, self.grid, self.components)

        # Only one thread should be running the script at a time, the script shouldn't be assumed
        # to be thread safe. If a thread is currently running the script when another is attempted
        # to be run, the new one will be added to the queue.
        self._thread = None
        self._thread_lock = threading.RLock()
        self._thread_running = False
        self._queue = queue.Queue()

    def start(self, scheduler):
        # Run setup hooks once
        for hook in self.hooks[HookEvent.Setup]:
            self.run_hook(hook)

        # Add scheduled tasks to the scheduler
        for hook in self.hooks[HookEvent.Schedule]:
            task = ScheduledTask(hook.schedule, callback=self.run_hook, args=[hook])
            scheduler.add_task(task)

    def run_hook(self, hook):
        """
        Adds the callback hook to the queue of the script.
        :param hook:
        """
        start_thread = False
        with self._thread_lock:
            self._queue.put_nowait(hook)
            if not self._thread_running:
                start_thread = True
                self._thread_running = True
        if start_thread:
            self.start_thread()

    def start_thread(self):
        while True:
            with self._thread_lock:
                if self._queue.empty():
                    self._thread_running = False
                    break
            hook = self._queue.get_nowait()
            self._thread = threading.Thread(target=hook.callback, args=[self.panel])
            self._thread.start()
            self._thread.join()


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

        script.start(scheduler)
