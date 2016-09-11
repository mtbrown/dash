import dash
from datetime import timedelta
from random import randint


@dash.hooks.setup
def setup(panel):
    panel.components['hello_text'].text = "This outputs random numbers"


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def loop(panel):
    panel.components['random_text'].text = str(randint(0, 99))
