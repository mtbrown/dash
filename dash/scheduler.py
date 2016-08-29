from datetime import timedelta, time


class Schedule:
    def __init__(self, run_every: timedelta = None, run_at: time = None, aligned: bool = False):
        """

        :param run_every: A timedelta object that describes how much time should pass between

        :param run_at:
        :param aligned:
        """
        self.run_every = run_every
        self.run_at = run_at
        self.aligned = aligned

        self.last_run = None  # the last time the task was run, or None if it hasn't been run
