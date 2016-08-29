import pytest

from dash.grid import parse_layout, Grid, BaseComponent
from dash.components.component import Component

# Sample layout declarations
valid_layout = """
    <Grid>
        <Row>
            <Col md=4>  <!-- test_col_a -->
                <Row>
                    <Col md=12><Statistic id="stat1" /></Col>
                    <Col md=12><Statistic id="stat2" /></Col>
                </Row>
            </Col>
            <Col md=8>
                <LineChart id="chart1" />
            </Col>
        </Row>
        <Row>
            <Col md=8>
                <BarChart id="chart2" />
            </Col>
            <Col md=4>
                <Table id="table" />
            </Col>
        </Row>
    </Grid>
    """


def test_parse_layout():
    """
    Test parsing a simple layout definition.
    """
    grid, component_list = parse_layout(valid_layout)

    assert isinstance(grid, Grid)

    assert len(component_list) == 5
    for component in component_list:
        assert isinstance(component, Component)

    assert len(grid.children) == 2
    assert len(grid.children[0].children) == 2

    test_col_a = grid.children[0].children[0]
    assert len(test_col_a.children) == 1
    assert test_col_a.md == 4

    stat1 = test_col_a.children[0].children[0].children[0]
    assert isinstance(stat1, BaseComponent)
    assert stat1.id == "stat1"


def test_grid_state():
    """
    Verify the representation of the grid state matches what the front-end expects.
    """
    grid, _ = parse_layout(valid_layout)

    assert grid.state == {
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
                    'id': 'chart1',
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
                    'id': 'chart2',
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
