import pytest
from dash.components import Text


def test_grid_basic(grid):
    assert grid.name == "test_grid"
    assert grid.num_columns == 1


def test_grid_add_remove_panel(grid):
    text_box = Text(title="Test", text="hello")
    grid.add(text_box)

    assert grid in text_box.containers
    assert text_box.id in grid.panel_columns
    assert grid.panel_columns[text_box.id] == 0  # should be added to first column by default
    assert text_box in grid.columns[0]

    grid.remove(text_box)

    assert grid not in text_box.containers
    assert text_box.id not in grid.panel_columns
    assert text_box not in grid.columns[0]
    assert len(grid.columns) == 1
    assert len(grid.columns[0]) == 0


def test_grid_set_num_columns(grid):
    assert grid.num_columns == 1
    grid.num_columns = 2
    assert grid.num_columns == 2
    grid.num_columns = 4
    assert grid.num_columns == 4

    grid.num_columns = 5  # invalid, must divide evenly into 12
    assert grid.num_columns == 4  # should ignore invalid value and stay at 4

    grid.num_columns = 2
    assert grid.num_columns == 2


def test_grid_add_remove_panels_multiple_columns(grid):
    num_columns = 3
    text_boxes = [Text(title="Text" + str(i)) for i in range(num_columns)]

    grid.num_columns = num_columns
    assert len(grid.columns) == num_columns

    for i in range(num_columns):
        grid.add(text_boxes[i], column=i)

    for i in range(num_columns):
        assert len(grid.columns[i]) == 1
        grid.remove(text_boxes[i])
        assert len(grid.columns[i]) == 0

