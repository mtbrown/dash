import pytest
import logging
from dash.grid import Grid


@pytest.fixture(autouse=True, scope='session')
def setup():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.DEBUG)


@pytest.fixture(scope='function')
def grid(request):
    return Grid(name="test_grid")
