import dash
from dash.components import ChartScale
from datetime import timedelta
import random

NUM_DATASETS = 5


def clamp(val, min_val, max_val):
    return min(max(val, min_val), max_val)


def random_walk(data):
    for i, val in enumerate(data):
        data[i] = clamp(val + random.randint(-10, 10), 0, 100)


@dash.hooks.setup
def setup(panel):
    panel.components['multiple_chart'].num_datasets = NUM_DATASETS
    panel.components['multiple_chart'].x_scale = ChartScale.Time

    bar_labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    for label in bar_labels:
        panel.components['bar_chart'].add_bar(label, random.randint(0, 100))

    panel.store['count'] = 0
    panel.store['data'] = [50 for _ in range(NUM_DATASETS)]


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def loop(panel):
    # Update basic line chart
    panel.components['basic_chart'].add_data(panel.store['count'], random.randint(0, 100))
    panel.store['count'] += 1

    # Update multiple dataset chart
    random_walk(panel.store['data'])
    panel.components['multiple_chart'].add_data_now(*panel.store['data'])

    # Update bar chart
    bar_chart = panel.components['bar_chart']
    bar_chart.update_bar(random.choice(bar_chart.labels), random.randint(0, 100))
