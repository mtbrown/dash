import dash
import time
import random
from datetime import timedelta


bar_labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]


@dash.hooks.setup
def main(panel):
    print(panel.components)
    for label in bar_labels:
        panel.components['bar_chart'].add_bar(label, random.randint(0, 100))

    panel.components['table'].headers = ["Time", "Value"]
    panel.components['table'].max_rows = 10


@dash.hooks.schedule(run_every=timedelta(seconds=1))
def update(panel):
    panel.components['stat1'].value = random.randint(0, 100)
    panel.components['stat2'].value = random.randint(0, 100)

    panel.components['line_chart'].add_point_now(random.randint(0, 20))
    panel.components['bar_chart'].update_bar(random.choice(bar_labels), random.randint(0, 100))

    panel.components['table'].add_row([str(time.time()), str(random.randint(0, 20))])


if __name__ == "__main__":
    pass
