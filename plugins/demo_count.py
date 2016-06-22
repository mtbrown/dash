from dash.components import LiveTextBox
import logging
import time


def main(grid):
    count = 0

    text_box = LiveTextBox(title="Counter")
    grid.add(text_box)

    while True:
        text_box.update("count is {0}".format(count))

        grid.logger.debug("count is {0}".format(count))
        count += 1
        time.sleep(1)


if __name__ == "__main__":
    pass
