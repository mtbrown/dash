from datetime import timedelta, time, datetime, date
import arrow


def next_time_occurrence(time: time, ref_datetime: arrow.Arrow = None):
    """
    Returns the next UTC date and time the specified UTC clock time will occur.
    The reference datetime will default to the current UTC datetime, but
    a custom datetime can be specified through the from_datetime parameter.
    If the current reference time matches the desired time exactly, the day
    will not be incremented and the untouched reference datetime will be returned.
    :param time: The desired clock time
    :param ref_datetime: The UTC datetime to use as the reference
    :return: The next datetime the desired clock time will occur
    """
    ref_datetime = ref_datetime if ref_datetime else arrow.utcnow()
    # move date to tomorrow if reference time has already passed desired time
    if ref_datetime.time() > time:
        ref_datetime = ref_datetime.replace(days=+1)
    combined = datetime.combine(ref_datetime.date(), time)
    return arrow.get(combined, 'utc')


def align_datetime(datetime: arrow.Arrow, timedelta: timedelta):
    """
    Align the provided datetime to the next datetime divisible by timedelta.
    :param datetime: The datetime to align
    :param timedelta: The interval of time to align to
    :return: The aligned datetime
    """
    base_time = arrow.get(0)
    remainder = (datetime - base_time) % timedelta
    aligned = datetime + timedelta - remainder
    return aligned


class Schedule:
    def __init__(self, run_every: timedelta, run_at: time = None, aligned: bool = False):
        """
        :param run_every: A timedelta object that describes how much time should pass between
        :param run_at:
        :param aligned:
        """
        self.run_every = run_every
        self.run_at = None
        self.aligned = aligned if run_at is None else False

        # Convert run_at from local timezone to UTC
        if run_at and run_every >= timedelta(days=1):
            # append run_at time to an arbitrary date in order to use arrow
            run_at_date = datetime.combine(date.today(), run_at)
            self.run_at = arrow.get(run_at_date, 'local').to('utc').time()

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
        self.next_run = self.last_run + self.run_every



