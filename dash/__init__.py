from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send
import eventlet

# monkey patching is required because background threads are used
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


@socketio.on('join', namespace='/api')
def on_join(data):
    join_room(data['room'])
    send("You have joined room {0}".format(data['room']))


@socketio.on('leave', namespace='/api')
def on_leave(data):
    leave_room(data['room'])


@app.template_filter('quote')
def quote(value):
    """Wraps the value in quotes. Intended for template use."""
    return '"{0}"'.format(value)
