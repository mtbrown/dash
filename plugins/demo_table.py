from dash.components import LiveTextBox, Table
from random import randint
import logging
import time


def main(grid):
    hello_text = LiveTextBox(title="Hello", text="This is a sample table")
    grid.add(hello_text)

    table = Table(title="Table", headers=["head1", "head2", "head3"], max_rows=10)
    table.rows = [["a1", "a2", "a3"], ["b1", "b2", "b3"], ["c1", "c2", "c3"]]
    grid.add(table)

    while True:
        new_row = [str(randint(0, 99)), str(randint(0, 99)), str(randint(0, 99))]
        table.add_row(new_row)
        time.sleep(1)


if __name__ == "__main__":
    pass
