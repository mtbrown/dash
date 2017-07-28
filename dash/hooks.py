"""
Hooks provide a means for user-written scripts to mark functions as execution entry points
or define custom callback functions for specific events.

Hooks are created through function decorators. When one of these decorators is applied
to a function, a ScriptHook object is attached to the function through the attribute
name specified by the ATTRIBUTE_NAME constant. This attached metadata to the function
which is later used by the script loader.
"""
from typing import Callable, List
from enum import Enum
from datetime import timedelta, datetime
import inspect
import os

from .scheduler import Schedule
from .script import Script


# The attribute used to attach the ScriptHook to the function.
ATTRIBUTE_NAME = '_script_hook'


class HookEvent(Enum):
    Setup = 'setup'
    Schedule = 'schedule'


class ScriptHook:
    def __init__(self, callback: Callable, event: HookEvent, schedule: Schedule = None):
        self.callback = callback
        self.event = event
        self.schedule = schedule


def load_hooks(script: Script) -> List[ScriptHook]:
    """
    Discovers the hooks defined within the provided directory. The directory
    is recursively searched and all files with a '.py' extension are inspected.
    A list of all ScriptHooks discovered within the directory is returned.
    :param script: 
    :return: A list of ScriptHooks that were discovered
    """
    hooks = []
    for name, func in inspect.getmembers(script.__class__, inspect.isfunction):
        if hasattr(func, ATTRIBUTE_NAME):
            hooks.append(getattr(func, ATTRIBUTE_NAME))
    return hooks


def setup(func):
    """
    Decorator used to mark a function to be called when the script is first loaded.
    """
    setattr(func, ATTRIBUTE_NAME, ScriptHook(func, HookEvent.Setup))
    return func


def schedule(run_every: timedelta = None, at: datetime = None, aligned: bool = False):
    """
    Decorator used to mark a function to be called at regular time intervals.
    :param run_every: The amount of time between successive calls.
    :param at: The time of day the function should be called. This is ignored if run_every
    is a timedelta of less than 1 day.
    :param aligned: If true, the call time will be aligned to the minimum unit specified
    in run_every; e.g, if run_every is a timedelta of 1 hour, the function will be called
    at the top of the hour, every hour. This parameter is ignored if 'at' is specified.
    """
    def decorator(func):
        schedule = Schedule(run_every=run_every, run_at=at, aligned=aligned)
        hook = ScriptHook(func, HookEvent.Schedule, schedule)
        setattr(func, ATTRIBUTE_NAME, hook)
        return func
    return decorator
