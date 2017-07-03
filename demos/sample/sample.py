import dash
from datetime import timedelta
from random import randint


@dash.hooks.setup
def setup(panel):
    # store is used for state storage across multiple executions
    panel.store['count'] = 0

    # perform one-time configuration UI components
    panel.components['table'].headers = ['Count', 'Value']
    panel.components['table'].max_rows = 10  # only store last 10 values
    panel.components['chart'].max_points = 10  # only plot last 10 values


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def update(panel):
    val = randint(0, 100)
    count = panel.store['count']  # retrieve current count

    panel.components['text'].text = 'The current value is: {0}'.format(val)
    panel.components['table'].add_row([count, val])
    panel.components['chart'].add_data(count, val)

    panel.store['count'] += 1
