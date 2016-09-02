import logging
from dash import start_server


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    start_server()

if __name__ == "__main__":
    main()
