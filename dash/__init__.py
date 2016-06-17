from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet
import logging

from . import plugins


logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s', level=logging.DEBUG)

# monkey patching is required because background threads are used
eventlet.monkey_patch()

socketio = SocketIO()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True

# load plugins
plugins.load_plugins()
plugin_list = plugins.list_plugins()
plugins.start_plugins()

# add url rules for all plugins
for plugin in plugin_list:
    app.add_url_rule("/{0}".format(plugin.name), plugin.name, plugin.view_func)


# add plugin list to template render environment
@app.context_processor
def inject_plugin_list():
    return {'plugins': {p.name for p in plugin_list}}


@app.route('/')
def index():
    return render_template('base.html', title="Dashboard")


socketio.init_app(app)

# Import views and socketio listeners, keep at bottom to avoid circular imports
import dash.systeminfo
