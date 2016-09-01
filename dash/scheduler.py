from datetime import timedelta, time, datetime, date
from typing import Callable, List, Dict
import arrow
import threading


def next_time_occurrence(time: time, tz: str = 'local', ref_datetime: arrow.Arrow = None):
    """
    Returns the next UTC date and time the specified local clock time will occur.
    The reference datetime will default to the current UTC datetime, but
    a custom datetime can be specified through the from_datetime parameter.
    If the current reference time matches the desired time exactly, the day
    will not be incremented and the untouched reference datetime will be returned.
    :param time: The desired local clock time
    :param tz: The timezone associated with the provided time, defaults to local
    :param ref_datetime: The UTC datetime to use as the reference
    :return: The next UTC datetime the desired local clock time will occur
    """
    ref_datetime = ref_datetime if ref_datetime else arrow.utcnow()
    local_ref_datetime = ref_datetime.to(tz)
    # move date to tomorrow if reference time has already passed desired time
    if local_ref_datetime.time() > time:
        local_ref_datetime = local_ref_datetime.replace(days=+1)
    combined = datetime.combine(local_ref_datetime.date(), time)
    return arrow.get(combined, tz).to('utc')


def align_datetime(datetime: arrow.Arrow, delta: timedelta, tz: str = 'local'):
    """
    Increase the provided datetime until it is aligned with a multiple of timedelta.
    The alignment will occur in the specified timezone, or the local timezone if unspecified.
    e.g., When the time delta is a day, the returned datetime will be the next
    midnight in the specified timezone. If the input datetime is already aligned,
    the output will be equivalent to the input.
    :param datetime: The datetime to align
    :param delta: The interval of time to align to
    :param tz: The reference timezone for alignment
    :return: The aligned datetime
    """
    # Convert to naive (no timezone) datetimes to force arithmetic using local times
    base_time = arrow.get(0).naive  # 1970-01-01T00:00:00
    local_time = datetime.to(tz).naive

    # Align naive datetime to next multiple of timedelta
    remainder = (local_time - base_time) % delta
    if remainder == timedelta(0):
        aligned_naive = local_time
    else:
        aligned_naive = local_time + delta - remainder

    # Convert back to aware (with timezone) datetime
    aligned = arrow.get(aligned_naive, tz)
    return aligned.to('utc')


class ScheduledTask(threading.Thread):
    def __init__(self, run_every: timedelta, callback: Callable, args: List = None,
                 kwargs: Dict = None, run_at: time = None, aligned: bool = False):
        """
        :param run_every: A timedelta object that describes how much time should pass between
        :param run_at:
        :param aligned:
        """
        super().__init__(target=callback, args=args, kwargs=kwargs)
        self.run_every = run_every
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        # run_at stored as a naive time in the local timezone
        self.run_at = run_at if self.run_every >= timedelta(days=1) else None
        self.aligned = aligned if run_at is None else False

        # last_run and next_run should be Arrow objects in UTC format
        self.last_run = None  # the last time the task was run, or None if it hasn't been run
        self.next_run = None

        # initialize self.next_run based on run_at and aligned
        if self.run_at:
            self.next_run = next_time_occurrence(self.run_at)
        elif self.aligned:
            self.next_run = align_datetime(arrow.utcnow(), self.run_every)
        else:
            self.next_run = arrow.utcnow()

    def update(self):
        self.last_run = self.next_run

        # The next_run datetime needs to be re-aligned every update
        # DST could have occurred in the local timezone since the last update
        next_run = self.last_run + self.run_every  # type: arrow.Arrow
        if self.run_at:
            self.next_run = next_time_occurrence(self.run_at, ref_datetime=next_run)
        elif self.aligned:
            self.next_run = align_datetime(next_run, self.run_every)
        else:
            self.next_run = next_run
