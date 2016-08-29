from typing import Callable
from enum import Enum
from datetime import timedelta, datetime

from .schedule import Schedule


class HookEvent(Enum):
    Setup = 'setup'
    Entry = 'entry'


class ScriptHook:
    def __init__(self, callback: Callable, event: HookEvent, schedule: Schedule = None):
        self.callback = callback
        self.event = event
        self.schedule = schedule


def setup(func):
    return ScriptHook(func, HookEvent.Setup)


def entry(run_every: timedelta = None, at: datetime = None, aligned: bool = False):
    def decorator(func):
        schedule = Schedule(run_every=run_every, run_at=at, aligned=aligned)
        return ScriptHook(func, HookEvent.Entry, schedule)
    return decorator
