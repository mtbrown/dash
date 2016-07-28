from dash.components import Text, BarChart, LineChart, ChartScale
import logging
import time
import random


def clamp(n, min_val, max_val):
    return max(min(max_val, n), min_val)


def main(grid):
    text_box = Text(title="Charts")
    grid.add(text_box)

    bar_labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"]
    bar_chart = BarChart(title="Sample Bar Chart")
    for label in bar_labels:
        bar_chart.add_bar(label, random.randint(0, 100))
    grid.add(bar_chart)

    line_chart = LineChart(title="Sample Line Chart", max_points=100)
    grid.add(line_chart)

    x = 0
    y = 50
    while True:
        line_chart.add_point(x, y)
        x += 1
        y += random.randint(-10, 10)
        y = clamp(y, 0, 100)

        bar_chart.update_bar(random.choice(bar_labels), random.randint(0, 100))

        time.sleep(1)


if __name__ == "__main__":
    pass
