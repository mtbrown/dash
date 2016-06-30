from flask import Flask, render_template
from flask_socketio import SocketIO
import eventlet

# monkey patching is required because background threads are used
eventlet.monkey_patch()

socketio = SocketIO()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug = True


@app.route('/')
def index():
    return render_template('base.html', title="Dashboard")

