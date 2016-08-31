import pytest
import arrow
from datetime import time, timedelta, datetime
from time import sleep

from dash.scheduler import Schedule, next_time_occurrence, align_datetime


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


def test_schedule_update_basic():
    schedule = Schedule(run_every=timedelta(hours=1))

    assert schedule.last_run is None
    start = schedule.next_run
    assert abs(start - arrow.utcnow()) < timedelta(minutes=1)

    schedule.update()
    assert schedule.last_run == start
    assert schedule.next_run == start + timedelta(hours=1)


def test_schedule_update_aligned():
    """
    Verify that an aligned schedule updates correctly.
    """
    # Test could generate a false negative if run near midnight and the
    # start time being stored and the schedule creation occurs on different days
    while abs(arrow.utcnow() - next_time_occurrence(time(0, 0, 0))) < timedelta(seconds=3):
        sleep(1)

    start = arrow.utcnow()
    schedule = Schedule(run_every=timedelta(days=1), aligned=True)
    expected_start = align_datetime(start, timedelta(days=1))
    assert schedule.next_run == expected_start

    schedule.update()
    assert schedule.next_run == expected_start + timedelta(days=1)


def test_schedule_update_run_at():
    """
    Verify that a schedule with a specified run time updates correctly.
    """
    # local time, converted to UTC inside of Schedule class
    desired_time = arrow.now().replace(hours=-1).time()

    schedule = Schedule(run_every=timedelta(days=1), run_at=desired_time)

    tomorrow = arrow.now().replace(days=+1)
    expected_next = arrow.get(datetime.combine(tomorrow.date(), desired_time), 'local').to('utc')
    assert schedule.next_run == expected_next

    schedule.update()
    assert schedule.next_run == expected_next + timedelta(days=1)

