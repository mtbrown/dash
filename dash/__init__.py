from flask import Flask
from flask_socketio import SocketIO
import eventlet
import os

from . import hooks

# monkey patching is required because background threads are used
eventlet.monkey_patch()

socketio = SocketIO()

app = Flask(__name__, static_url_path='', static_folder='../client/public')
app.config['SECRET_KEY'] = 'secret!'
app.debug = True

from .scripts import ScriptManager
scripts_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "scripts"))  # ../scripts

# start a separate thread to monitor the status of running scripts
script_manager = ScriptManager(scripts_path)
script_manager.start()

from .api import api
app.register_blueprint(api.blueprint, url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')
