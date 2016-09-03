import dash
from datetime import timedelta


@dash.hooks.setup
def setup(panel):
    print("Hello")


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def update_seconds(panel):
    secs_stat = panel.components['secs']
    secs_stat.value = (secs_stat.value + 1) % 60


@dash.hooks.schedule(run_every=timedelta(minutes=1))
def update_minutes(panel):
    panel.components['mins'].value += 1
