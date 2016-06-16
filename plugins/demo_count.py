from dash.panel import Panel, LiveTextBox
import time


def main(panel):
    count = 0

    text_box = LiveTextBox()
    panel.add(text_box)

    while True:
        # update

        count += 1
        time.sleep(1)


if __name__ == "__main__":
    main(Panel())
