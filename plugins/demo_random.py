from dash.components import LiveTextBox
from random import randint
import logging
import time


def main(grid):
    hello_text = LiveTextBox(title="Hello", text="This outputs random numbers")
    grid.add(hello_text)

    rand_text = LiveTextBox(title="Random")
    grid.add(rand_text)

    while True:
        rand_text.update(str(randint(0, 99)))
        time.sleep(1)


if __name__ == "__main__":
    pass
