from dash.components import Text
from random import randint
import logging
import time


def main(grid):
    hello_text = Text(title="Hello", text="This outputs random numbers")
    grid.add(hello_text)

    rand_text = Text(title="Random")
    grid.add(rand_text)

    while True:
        rand_text.update(str(randint(0, 99)))
        time.sleep(1)


if __name__ == "__main__":
    pass
