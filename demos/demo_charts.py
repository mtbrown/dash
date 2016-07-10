from dash.components import Text, BarChart, LineChart
import logging
import time
from random import randint


def clamp(n, min_val, max_val):
    return max(min(max_val, n), min_val)


def main(grid):
    text_box = Text(title="Charts")
    grid.add(text_box)

    bar_chart = BarChart(title="Sample Bar Chart", labels=("Red", "Blue", "Yellow", "Green", "Purple", "Orange"))
    grid.add(bar_chart)

    line_chart = LineChart(title="Sample Line Chart", max_points=100)
    grid.add(line_chart)

    x = 0
    y = 50
    while True:
        line_chart.add_data(x, y)
        x += 1
        y += randint(-10, 10)
        y = clamp(y, 0, 100)
        time.sleep(1)


if __name__ == "__main__":
    pass
