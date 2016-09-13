from datetime import timedelta, time, datetime
from typing import Callable, List, Dict, Tuple
from time import sleep
import arrow
import threading
import heapq


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


class Schedule:
    def __init__(self, run_every: timedelta, run_at: time = None, aligned: bool = False, tz: str = 'local'):
        self.run_every = run_every
        self.run_at = run_at if self.run_every >= timedelta(days=1) else None
        self.aligned = aligned if run_at is None else False
        self.tz = tz

        # last_run and next_run should be Arrow objects in UTC format
        self.last_run = None  # the last time the task was run, or None if it hasn't been run
        self.next_run = None

        # initialize self.next_run based on run_at and aligned
        if self.run_at:
            self.next_run = next_time_occurrence(self.run_at, tz=self.tz)
        elif self.aligned:
            self.next_run = align_datetime(arrow.utcnow(), self.run_every, tz=self.tz)
        else:
            self.next_run = arrow.utcnow()

    def update(self):
        self.last_run = self.next_run

        # The next_run datetime needs to be re-aligned every update
        # DST could have occurred in the local timezone since the last update
        next_run = self.last_run + self.run_every  # type: arrow.Arrow
        if self.run_at:
            self.next_run = next_time_occurrence(self.run_at, tz=self.tz, ref_datetime=next_run)
        elif self.aligned:
            self.next_run = align_datetime(next_run, self.run_every, tz=self.tz)
        else:
            self.next_run = next_run


class ScheduledTask:
    def __init__(self, schedule: Schedule, callback: Callable, args: List = None, kwargs: Dict = None):
        self.schedule = schedule
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        self.thread = None

    @property
    def next_run(self):
        return self.schedule.next_run

    def run(self):
        self.thread = threading.Thread(target=self.callback, args=self.args, kwargs=self.kwargs)
        self.thread.start()
        self.schedule.update()


class Scheduler(threading.Thread):
    def __init__(self):
        super().__init__()

        self._queue = []  # type: List[Tuple[arrow.Arrow, int, ScheduledTask]]
        self._queue_lock = threading.RLock()
        self._stop_event = threading.Event()

        # The counter is added to the entry tuple for every task added to the queue.
        # This breaks ties between equivalent next_run times and guarantees that
        # the ScheduledTask objects will never be compared.
        self._counter = 0
        self._counter_lock = threading.RLock()

    def add_task(self, task: ScheduledTask):
        with self._counter_lock:
            entry = (task.next_run, self._counter, task)  # wrap in tuple to force sorting by next_run
            self._counter += 1
        with self._queue_lock:
            heapq.heappush(self._queue, entry)

    def stop(self):
        self._stop_event.set()

    def run(self):
        while not self._stop_event.is_set():
            with self._queue_lock:
                next = self._queue[0][2] if self._queue else None  # type: ScheduledTask

            if next:
                now = arrow.utcnow()
                if now >= next.next_run:
                    next.run()
                    with self._queue_lock:
                        heapq.heappop(self._queue)
                    self.add_task(next)
                else:
                    # set an upper limit on sleep time
                    # another task could be added that occurs before current next
                    sleep_delta = min(next.next_run - now, timedelta(seconds=0.5))
                    sleep(sleep_delta.total_seconds())
            else:
                sleep(0.5)

    def __len__(self):
        with self._queue_lock:
            return len(self._queue)
