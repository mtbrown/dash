from dash.components import Text
import logging
import time
import random


def main(grid):
    num_columns = 3  # must be a factor of 12
    text_boxes = [Text(title="Column " + str(i)) for i in range(num_columns)]

    grid.num_columns = num_columns
    for i, text_box in enumerate(text_boxes):
        grid.add(text_box, column=i)

    while True:
        for text_box in text_boxes:
            text_box.update(str(random.randint(0, 100)))

        time.sleep(1)

if __name__ == "__main__":
    pass
