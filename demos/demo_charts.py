from dash.components import Text, BarChart
import logging
import time


def main(grid):
    text_box = Text(title="Charts")
    grid.add(text_box)

    bar_chart = BarChart()
    grid.add(bar_chart)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    pass
