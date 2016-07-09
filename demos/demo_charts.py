from dash.components import Text, BarChart, LineChart
import logging
import time


def main(grid):
    text_box = Text(title="Charts")
    grid.add(text_box)

    bar_chart = BarChart(title="Sample Bar Chart", labels=("Red", "Blue", "Yellow", "Green", "Purple", "Orange"))
    grid.add(bar_chart)

    line_chart = LineChart(title="Sample Line Chart", labels=("Red", "Blue", "Yellow", "Green", "Purple", "Orange"))
    grid.add(line_chart)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    pass
