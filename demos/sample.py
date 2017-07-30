import dash
from dash.grid import Grid, Col, Row
from dash.components import Text, Table, LineChart

from datetime import timedelta
from random import randint


class DemoGrid(dash.Script):
    def __init__(self):
        super().__init__(id='sample')

        self.count = 0

        # Component definitions
        self.text = Text(id='sample_text')
        self.table = Table(id='table', headers=['Count', 'Value'], max_rows=10)
        self.chart = LineChart(id='chart', max_points=10)

    @dash.hooks.schedule(run_every=timedelta(seconds=1))
    def update(self):
        val = randint(0, 100)  # generate new value

        self.text.text = 'The current value is: {0}'.format(val)
        self.table.add_row([self.count, val])
        self.chart.add_data(self.count, val)

        self.count += 1

    def render(self):
        return Grid(
            Row(
                Col(self.text, md=12),
            ),
            Row(
                Col(self.table, md=6),
                Col(self.chart, md=6)
            )
        )
