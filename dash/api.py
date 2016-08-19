from flask_restful import Api, Resource
from flask import Blueprint
from flask_socketio import join_room, leave_room, send

from . import socketio
from .plugins import list_plugins, get_script_by_id
from .components.panel import get_component_by_id


api = Api(Blueprint('api', __name__))


@socketio.on('join', namespace='/api')
def on_join(data):
    join_room(data['room'])
    send("You have joined room {0}".format(data['room']))


@socketio.on('leave', namespace='/api')
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
        } for script in list_plugins()]


@api.resource('/scripts/<script_id>/grid')
class ScriptGrid(Resource):
    @staticmethod
    def get(script_id):
        response = []
        try:
            script = get_script_by_id(script_id)
        except ValueError:
            return {"error": "Invalid script ID: {0}".format(script_id)}, 400

        for column in script.grid.columns:
            response.append([{
                "id": component.id,
                "type": component.__class__.__name__
            } for component in column])
        return {"columns": response}


@api.resource('/components/<component_id>')
class Component(Resource):
    @staticmethod
    def get(component_id):
        try:
            component = get_component_by_id(component_id)
        except ValueError:
            return {"error": "Invalid component ID: {0}".format(component_id)}, 400
        return component.state
