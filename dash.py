from dash import app, socketio

if __name__ == "__main__":
    socketio.run(app, use_reloader=False)
