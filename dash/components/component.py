import abc
#from .. import socketio


component_id_map = {}


class Component:
    __metaclass__ = abc.ABCMeta

    id_counter = 0

    def __init__(self, title=None):
        self.title = title
        self.containers = []  # grids that panel is currently contained in
        self.id = Component.id_counter
        component_id_map[str(self.id)] = self
        Component.id_counter += 1

    @abc.abstractproperty
    def state(self):
        return {}

    def emit_state(self):
        pass
        #socketio.emit(self.id, self.state, namespace='/api', room=self.id)


def get_component_by_id(component_id):
    return component_id_map[component_id]
