from flask import Flask
import eventlet
import os
from datetime import timedelta

# Monkey patch standard library to work with eventlet
# http://eventlet.net/doc/patching.html
eventlet.monkey_patch()

from .scheduler import Schedule, Scheduler, ScheduledTask
from .scripts import load_scripts
from .api import api, socket
from . import hooks
from .script import Script

# Path that contains scripts
SCRIPTS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "scripts"))  # ../scripts

app = Flask(__name__, static_url_path='', static_folder='../client/public')
app.config['SECRET_KEY'] = 'secret!'
app.debug = True

app.register_blueprint(api.blueprint, url_prefix='/api')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('index.html')


def start_server():
    schedule = Scheduler()
    load_scripts_task = ScheduledTask(Schedule(run_every=timedelta(minutes=1)),
                                      callback=load_scripts, args=[SCRIPTS_PATH, schedule])
    schedule.add_task(load_scripts_task)
    schedule.start()

    socket.init_app(app)
    socket.run(app, use_reloader=False, host='0.0.0.0')

