import pytest
import arrow
from datetime import time, timedelta

from dash.scheduler import next_time_occurrence, align_datetime


def test_next_time_occurrence():
    # Basic usage with a time later in the day
    assert next_time_occurrence(time(hour=22, minute=30, second=11),
                                ref_datetime=arrow.get('2016-08-30T20:42:41.737733+00:00')) \
        == arrow.get('2016-08-30T22:30:11.000000+00:00')

    # Time specified has already passed, should roll over to tomorrow
    assert next_time_occurrence(time(hour=8, minute=22),
                                ref_datetime=arrow.get('2016-08-30T20:42:41.737733+00:00')) \
        == arrow.get('2016-08-31T08:22:00.000000+00:00')

    # Day rollover should result in a month rollover
    assert next_time_occurrence(time(hour=8, minute=21),
                                ref_datetime=arrow.get('2016-08-31T08:22:00.000000+00:00')) \
        == arrow.get('2016-09-01T08:21:00.000000+00:00')

    # If times match exactly, day shouldn't roll over
    assert next_time_occurrence(time(hour=8, minute=21),
                                ref_datetime=arrow.get('2016-08-31T08:21:00.000000+00:00')) \
        == arrow.get('2016-08-31T08:21:00.000000+00:00')


def test_align_datetime():
    assert align_datetime(arrow.get('2016-08-30T20:42:41.737733+00:00'), timedelta(hours=1)) \
           == arrow.get('2016-08-30T21:00:00.000000+00:00')

    assert align_datetime(arrow.get('2016-08-31T20:42:41.737733+00:00'), timedelta(days=1)) \
           == arrow.get('2016-09-01T00:00:00.000000+00:00')
