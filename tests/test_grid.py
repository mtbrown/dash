import pytest

import dash
from dash.grid import Grid, Col, Row
from dash.components import Statistic, LineChart, BarChart, Table


def test_grid_context_manager_state():
    """
    Verify the representation of the grid state matches what the front-end expects.
    """
    class DemoGrid(dash.App):
        def __init__(self):
            super().__init__()

            self.stat_1 = Statistic(id='stat1')
            self.stat_2 = Statistic(id='stat2')
            self.line_chart = LineChart(id='line_chart', min_y=0, max_y=20)
            self.bar_chart = BarChart(id='bar_chart', min_y=0, max_y=100)
            self.table = Table(id='table')

        def render(self):
            return Grid(
                Row(
                    Col(
                        Row(
                            Col(self.stat_1, md=12),
                            Col(self.stat_2, md=12)
                        ),
                        md=4,
                    ),
                    Col(self.line_chart, md=8)
                ),
                Row(
                    Col(self.bar_chart, md=8),
                    Col(self.table, md=4)
                )
            )

    test = DemoGrid()

    assert test.render().state == {
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
