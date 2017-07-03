import pytest

from dash.grid import Grid, Col, Row
from dash.components import Statistic, LineChart, BarChart, Table


class DemoGrid:
    def __init__(self):
        self.grid = Grid()

        with self.grid:
            with Row():
                with Col(md=4):
                    with Row():
                        with Col(md=12):
                            self.stat_1 = Statistic(id='stat1')
                        with Col(md=12):
                            self.stat_2 = Statistic(id='stat2')
                with Col(md=8):
                    self.line_chart = LineChart(id='line_chart', min_y=0, max_y=20)
            with Row():
                with Col(md=8):
                    self.bar_chart = BarChart(id='bar_chart', min_y=0, max_y=100)
                with Col(md=4):
                    self.table = Table(id='table')


def test_grid_state():
    """
    Verify the representation of the grid state matches what the front-end expects.
    """
    test = DemoGrid()

    assert test.grid.state == {
        'children': [{
            'children': [{
                'props': {
                    'md': 4
                },
                'children': [{
                    'children': [{
                        'props': {
                            'md': 12
                        },
                        'children': [{
                            'id': 'stat1',
                            'type': 'Statistic'
                        }],
                        'type': 'Col'
                    }, {
                        'props': {
                            'md': 12
                        },
                        'children': [{
                            'id': 'stat2',
                            'type': 'Statistic'
                        }],
                        'type': 'Col'
                    }],
                    'type': 'Row'
                }],
                'type': 'Col'
            }, {
                'props': {
                    'md': 8
                },
                'children': [{
                    'id': 'line_chart',
                    'type': 'LineChart'
                }],
                'type': 'Col'
            }],
            'type': 'Row'
        }, {
            'children': [{
                'props': {
                    'md': 8
                },
                'children': [{
                    'id': 'bar_chart',
                    'type': 'BarChart'
                }],
                'type': 'Col'
            }, {
                'props': {
                    'md': 4
                },
                'children': [{
                    'id': 'table',
                    'type': 'Table'
                }],
                'type': 'Col'
            }],
            'type': 'Row'
        }],
        'type': 'Grid'
    }
