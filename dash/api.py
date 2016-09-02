from flask_restful import Api, Resource
from flask import Blueprint
from flask_socketio import SocketIO, join_room, leave_room, send

from . import scripts

socket = SocketIO()

api = Api(Blueprint('api', __name__))


@socket.on('join', namespace='/api')
def on_join(data):
    join_room(data['room'])
    send("You have joined room {0}".format(data['room']))


@socket.on('leave', namespace='/api')
def on_leave(data):
    leave_room(data['room'])


@api.resource('/scripts')
class Scripts(Resource):
    @staticmethod
    def get():
        return [{
            "id": script.id,
            "title": script.title,
            "status": script.status.value,
            "label": str(script.label)
        } for script in scripts.script_list]


@api.resource('/scripts/<script_id>/grid')
class ScriptGrid(Resource):
    @staticmethod
    def get(script_id):
        try:
            script = scripts.script_map[script_id]
        except ValueError:
            return {"error": "Invalid script ID: {0}".format(script_id)}, 400

        return script.grid.state


@api.resource('/scripts/<script_id>/components/<component_id>')
class Component(Resource):
    @staticmethod
    def get(script_id, component_id):
        try:
            script = scripts.script_map[script_id]
            component = script.components[component_id]
        except ValueError:
            return {"error": "Invalid component ID: {0}".format(component_id)}, 400
        return component.state
