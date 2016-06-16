from dash import app, socketio, plugins

if __name__ == "__main__":
    plugins.load_plugins()
    socketio.run(app)
