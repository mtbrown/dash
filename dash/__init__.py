from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

# monkey patching is required because background threads are used
eventlet.monkey_patch()

socketio = SocketIO()

app = Flask(__name__, static_url_path='', static_folder='../client/public')
app.config['SECRET_KEY'] = 'secret!'
app.debug = True


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    app.send_static_file('index.html')


@app.template_filter('quote')
def quote(value):
    """Wraps the value in quotes. Intended for template use."""
    return '"{0}"'.format(value)
