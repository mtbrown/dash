import random
from datetime import timedelta
import time

import dash
from dash.grid import Grid, Col, Row
from dash.components import BarChart, Table, Statistic, LineChart


bar_labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]


class DemoGrid(dash.App):
    def __init__(self):
        self.grid = Grid()

        with self.grid:
            with Row():
                with Col(md=4):
                    with Row():
                        with Col(md=12):
                            self.stat_1 = Statistic(id='stat_1')
                        with Col(md=12):
                            self.stat_2 = Statistic(id='stat_2')
                with Col(md=8):
                    self.line_chart = LineChart(id='line_chart', min_y=0, max_y=20)
            with Row():
                with Col(md=8):
                    self.bar_chart = BarChart(id='bar_chart', min_y=0, max_y=100)
                with Col(md=4):
                    self.table = Table(id='table', headers=['Time', 'Value'], max_rows=10)

        for label in bar_labels:
            self.bar_chart.add_bar(label, random.randint(0, 100))

    @dash.hooks.schedule(run_every=timedelta(seconds=1))
    def update(self, panel):
        self.stat_1.value = random.randint(0, 100)
        self.stat_2.value = random.randint(0, 100)

        self.line_chart.add_data_now(random.randint(0, 20))
        self.bar_chart.update_bar(random.choice(bar_labels), random.randint(0, 100))

        self.table.add_row([str(time.time()), str(random.randint(0, 20))])
