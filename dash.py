from dash import app, socketio, plugins, systeminfo


def main():
    # load plugins
    plugins.load_plugins()
    plugin_list = plugins.list_plugins()
    plugins.start_plugins()

    # add plugin list to template renderer environment
    @app.context_processor
    def inject_plugin_list():
        return {'plugins': {p.name for p in plugin_list}}

    socketio.init_app(app)
    socketio.run(app, use_reloader=False)

if __name__ == "__main__":
    main()
