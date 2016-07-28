import abc
from .. import socketio


class Panel:
    id_counter = 0

    def __init__(self, title=None):
        self.title = title
        self.containers = []  # grids that panel is currently contained in
        self.id = "panel" + str(Panel.id_counter)
        Panel.id_counter += 1

    @abc.abstractmethod
    def render_html(self):
        return

    @abc.abstractmethod
    def render_js(self):
        return

    def emit(self, data):
        """Emit a SocketIO message to each grid that this panel is currently contained in."""
        for container in self.containers:
            socketio.emit(self.id, data, namespace='/' + container.name)
