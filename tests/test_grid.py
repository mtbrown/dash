import pytest
from dash.components import Text


def test_grid_basic(grid):
    """Verify basic properties of a default grid."""
    assert grid.name == "test_grid"
    assert grid.num_columns == 1
    assert grid.column_size == 12


def test_grid_add_remove_panel(grid):
    """Verify that a panel can be added to and removed from a simple, single-column grid."""
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
    """Verify that num_columns cannot be set to invalid values. A valid value must be a factor of 12."""
    assert grid.num_columns == 1
    grid.num_columns = 2
    assert grid.num_columns == 2
    grid.num_columns = 4
    assert grid.num_columns == 4

    grid.num_columns = 5  # invalid, must divide evenly into 12
    assert grid.num_columns == 4  # should ignore invalid value and stay at 4
    grid.num_columns = 0  # invalid, must be positive
    assert grid.num_columns == 4
    grid.num_columns = -1  # invalid, must be positive
    assert grid.num_columns == 4
    grid.num_columns = 13  # invalid, must be 12 or less
    assert grid.num_columns == 4

    grid.num_columns = 2
    assert grid.num_columns == 2


def test_grid_column_size_update(grid):
    """Verify that the column_size properly updates along with num_columns."""
    assert grid.column_size == 12

    grid.num_columns = 3
    assert grid.column_size == 4
    grid.num_columns = 6
    assert grid.column_size == 2
    grid.num_columns = 12
    assert grid.column_size == 1


def test_grid_add_remove_panels_multiple_columns(grid):
    """Verify that panels are properly added to and removed from the correct column
    when there are multiple columns."""
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


def test_grid_add_panel_column_out_of_range(grid):
    """Verify that panels cannot be added to a column that doesn't exist in the grid."""
    grid.num_columns = 4
    text_box = Text()
    grid.add(text_box, column=-1)
    grid.add(text_box, column=4)

    for column in grid.columns:
        assert len(column) == 0
    assert len(text_box.containers) == 0


def test_grid_add_duplicate_panels(grid):
    """Verify that when adding a duplicate panel to a grid, the second add is ignored."""
    text_box = Text(title="Test", text="Hello")

    grid.add(text_box, column=0)
    grid.add(text_box, column=0)

    assert len(grid.columns[0]) == 1
    assert len(text_box.containers) == 1


def test_grid_double_remove_panel(grid):
    """Verify that when removing a panel from grid twice, the second remove is ignored."""
    text_box = Text(title="Test", text="Hello")

    grid.add(text_box, column=0)
    assert len(grid.columns[0]) == 1
    assert len(text_box.containers) == 1

    grid.remove(text_box)
    grid.remove(text_box)
    assert len(grid.columns[0]) == 0
    assert len(text_box.containers) == 0


def test_grid_reduce_columns_remove_panels(grid):
    """Verify that when the number of columns is reduced, the panels in the rightmost columns
    that are deleted are removed from the grid."""
    text_box1 = Text(title="Test1")
    text_box2 = Text(title="Test2")

    grid.num_columns = 4
    grid.add(text_box1, column=0)
    grid.add(text_box2, column=3)

    grid.num_columns = 1

    assert len(grid.columns) == 1
    assert len(grid.columns[0]) == 1
    assert len(text_box1.containers) == 1  # should remain in grid
    assert len(text_box2.containers) == 0  # should have been removed from grid
