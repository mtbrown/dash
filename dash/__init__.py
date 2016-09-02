from flask import Flask
from flask_socketio import SocketIO
import eventlet
import os
from datetime import timedelta

from .scheduler import Scheduler, ScheduledTask
from .scripts import load_scripts

# Path that contains scripts
SCRIPTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "scripts"))  # ../scripts

# eventlet is required for flask_socketio
# monkey patching is required because threading is used
eventlet.monkey_patch()

socketio = SocketIO()

app = Flask(__name__, static_url_path='', static_folder='../client/public')
app.config['SECRET_KEY'] = 'secret!'
app.debug = True

from .api import api
app.register_blueprint(api.blueprint, url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')


def start_server():
    schedule = Scheduler()
    load_scripts_task = ScheduledTask(run_every=timedelta(minutes=1), callback=load_scripts,
                                      args=[SCRIPTS_PATH])
    schedule.add_task(load_scripts_task)
    schedule.start()
