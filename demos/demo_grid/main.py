from dash.components import Statistic, LineChart, BarChart, Table
import logging
import time
import random


def main(panel):
    stat1 = panel.components['stat1']  # type: Statistic
    stat2 = panel.components['stat2']  # type: Statistic
    bar_chart = panel.components['chart2']  # type: BarChart
    line_chart = panel.components['chart1']  # type: LineChart
    table = panel.components['table']  # type: Table

    bar_labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    for label in bar_labels:
        bar_chart.add_bar(label, random.randint(0, 100))

    table.headers = ["Time", "Value"]
    table.max_rows = 10

    while True:
        stat1.value = random.randint(0, 100)
        stat2.value = random.randint(0, 100)

        line_chart.add_point_now(random.randint(0, 20))
        bar_chart.update_bar(random.choice(bar_labels), random.randint(0, 100))

        table.add_row([str(time.time()), str(random.randint(0, 20))])

        time.sleep(1)

if __name__ == "__main__":
    pass
