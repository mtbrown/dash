import enum
import os
import queue
import threading

from .hooks import HookEvent, load_hooks
from .scheduler import ScheduledTask
from .script import Script, load_script

script_list = []

script_map = {}

script_path_map = {}


class ScriptStatus(enum.Enum):
    Ok = "ok"
    Warning = "warning"
    Error = "error"


class ScriptExecution:
    def __init__(self, id: str, script: Script):
        self.id = id  # name of module/package containing script
        self.script = script

        self.grid = script.render()
        self.title = id  # title displayed
        self.status = ScriptStatus.Ok
        self.label = 0

        self.components = {comp.id: comp for comp in self.grid.components}

        self.hooks = {event: [] for event in HookEvent}
        for hook in load_hooks(self.script):
            self.hooks[hook.event].append(hook)

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
            self._thread = threading.Thread(target=hook.callback, args=[self.script])
            self._thread.start()
            self._thread.join()


def load_scripts(path, scheduler):
    for sub_path in os.listdir(path):
        if sub_path in {'__pycache__'}:
            continue

        name, _ = os.path.splitext(sub_path)
        script_path = os.path.join(path, sub_path)

        script = load_script(script_path)
        if script is None or script_path in script_path_map:
            continue

        script = ScriptExecution(name, script)
        script_list.append(script)
        script_map[script.id] = script
        script_path_map[script_path] = script

        script.start(scheduler)
