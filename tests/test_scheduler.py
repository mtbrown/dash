import pytest
import arrow
from datetime import time, timedelta, datetime
from time import sleep

from dash.scheduler import Scheduler, ScheduledTask, next_time_occurrence, align_datetime


def test_next_time_occurrence():
    """
    Verify correct functionality of next_time_occurrence().
    """
    # Using default 'local' timezone would result in inconsistent tests
    test_tz = 'America/Los_Angeles'
    test_time = arrow.get('2016-08-30T13:42:41.737733-07:00')

    # Basic usage with a time later in the day
    assert next_time_occurrence(time(hour=22, minute=30, second=11), tz=test_tz,
                                ref_datetime=test_time) \
        == test_time.replace(hour=22, minute=30, second=11, microsecond=0)

    # Time specified has already passed, should roll over to tomorrow
    assert next_time_occurrence(time(hour=8, minute=22), tz=test_tz,
                                ref_datetime=test_time) \
        == test_time.replace(days=+1, hour=8, minute=22, second=0, microsecond=0)

    # Day rollover should result in a month rollover
    test_time = test_time.replace(days=+1)  # increment day
    assert next_time_occurrence(time(hour=8, minute=22), tz=test_tz,
                                ref_datetime=test_time) \
        == arrow.get("2016-09-01T08:22:00.000000-07:00")

    # If times match exactly, day shouldn't roll over
    test_time = arrow.get("2016-09-01T08:21:00.000000-07:00")
    assert next_time_occurrence(time(hour=8, minute=21), tz=test_tz,
                                ref_datetime=test_time) \
        == test_time


def test_align_datetime():
    """
    Verify correct functionality of align_datetime().
    """
    test_tz = 'America/Los_Angeles'

    assert align_datetime(arrow.get('2016-08-31T18:44:03.327717-07:00'),
                          timedelta(hours=1), tz=test_tz) \
        == arrow.get('2016-08-31T19:00:00.000000-07:00')

    assert align_datetime(arrow.get('2016-08-31T18:44:03.327717-07:00'),
                          timedelta(days=1), tz=test_tz) \
        == arrow.get('2016-09-01T00:00:00.000000-07:00')

    assert align_datetime(arrow.get('2016-08-31T18:44:03.327717-07:00'),
                          timedelta(hours=3), tz=test_tz) \
        == arrow.get('2016-08-31T21:00:00.000000-07:00')

    # Already aligned datetime should result in the same time as output
    assert align_datetime(arrow.get('2016-08-31T21:00:00.000000-07:00'),
                          timedelta(hours=3), tz=test_tz).to('local') \
        == arrow.get('2016-08-31T21:00:00.000000-07:00')


def test_schedule_update_basic():
    """
    Verify that a basic schedule updates correctly.
    """
    schedule = ScheduledTask(run_every=timedelta(hours=1), callback=lambda x: x)

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
    schedule = ScheduledTask(run_every=timedelta(days=1), callback=lambda x: x, aligned=True)
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

    schedule = ScheduledTask(run_every=timedelta(days=1), callback=lambda x: x, run_at=desired_time)

    tomorrow = arrow.now().replace(days=+1)
    expected_next = arrow.get(datetime.combine(tomorrow.date(), desired_time), 'local')
    assert schedule.next_run == expected_next

    schedule.update()
    assert schedule.next_run == expected_next + timedelta(days=1)


def test_scheduler_basic():
    """
    Add two tasks to a scheduler and verify that the times the callback function
    is called is close to the expected times.
    """
    scheduler = Scheduler()

    call_times = {
        'a': [],
        'b': []
    }

    expected_times = {
        'a': [0, 1, 2, 3],
        'b': [0, 0.5, 1, 1.5, 2, 2.5, 3]
    }

    def test_callback(id):
        call_times[id].append(arrow.now())

    task1 = ScheduledTask(run_every=timedelta(seconds=1), callback=test_callback, args=['a'])
    task2 = ScheduledTask(run_every=timedelta(seconds=0.5), callback=test_callback, args=['b'])

    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.start()
    start = arrow.now()
    sleep(3.5)
    scheduler.stop()

    for id in expected_times:
        assert len(call_times[id]) >= len(expected_times[id])
        for call_time, expected in zip(call_times[id], expected_times[id]):
            call_delta = call_time - start
            expected_delta = timedelta(seconds=expected)
            assert abs(call_delta - expected_delta) <= timedelta(seconds=0.5)
