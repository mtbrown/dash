import json
import enum
from functools import wraps
from flask_restful import Api, Resource
from flask import Blueprint

from .plugins import list_plugins, get_script_by_id
from .components.panel import get_component_by_id


api = Api(Blueprint('api', __name__))


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


# @socket.on('connect', namespace='/api')
def test_connect():
    print("Connected successfully")


# @socket.on('message', namespace='/api')
def message_handler(message):
    print("Received: " + str(message))

    if type(message) is dict:
        json_message = message
    elif type(message) is str:
        try:
            json_message = json.loads(message)
        except ValueError:
            print("Error parsing json")
            return
    else:
        print("Invalid message type")
        return
