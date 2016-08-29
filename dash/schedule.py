from datetime import timedelta, datetime


class Schedule:
    def __init__(self, run_every: timedelta = None, run_at: datetime = None, aligned: bool = False):
        self.run_every = run_every
        self.run_at = run_at
        self.aligned = aligned

        self.last_run = None
