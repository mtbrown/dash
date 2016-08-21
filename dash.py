import logging
from dash import app, socketio


def main():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.INFO)

    socketio.init_app(app)
    socketio.run(app, use_reloader=False, host='0.0.0.0')

if __name__ == "__main__":
    main()
