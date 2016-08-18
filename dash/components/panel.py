import abc
from .. import socketio


component_id_map = {}


class Panel:
    __metaclass__ = abc.ABCMeta

    id_counter = 0

    def __init__(self, title=None):
        self.title = title
        self.containers = []  # grids that panel is currently contained in
        self.id = Panel.id_counter
        component_id_map[str(self.id)] = self
        Panel.id_counter += 1

    @abc.abstractproperty
    def state(self):
        return {}

    def emit_state(self):
        socketio.emit(self.id, self.state, namespace='/api', room=self.id)

    def emit(self, data):
        """Emit a SocketIO message to each grid that this panel is currently contained in."""
        for container in self.containers:
            socketio.emit(self.id, data, namespace='/' + container.name)


def get_component_by_id(component_id):
    return component_id_map[component_id]
