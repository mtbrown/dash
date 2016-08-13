import json
import enum
from functools import wraps
import flask

from . import socketio as socket
from .plugins import list_plugins


request_handlers = {}


class RequestAction(enum.Enum):
    Create = "create"
    Retrieve = "retrieve"
    Update = "update"
    Delete = "delete"
    Flush = "flush"


class ResponseStatus(enum.Enum):
    Success = "success"  # all went well, some data was returned
    Fail = "fail"  # there was a problem with the request
    Error = "error"  # an error occurred when processing the request


# Binds a handler function to a specific request action and target combination
def bind_handler(target, action):
    def decorator(func):
        @wraps(func)  # preserve wrapped function's metadata
        def wrapper(*args, **kwargs):
            status, response = func(*args, **kwargs)  # get generated response from handler
            message = json.dumps({
                "status": status.value,
                "response": response
            })
            socket.emit(target, message, namespace='/api')  # emit response
        request_handlers[(action, target)] = wrapper  # bind newly wrapped function
        return wrapper
    return decorator


@bind_handler("script_list", RequestAction.Retrieve)
def get_script_list(request):
    response = []
    for script in list_plugins():
        response.append({
            "id": script.name
        })
    return ResponseStatus.Success, {"scripts": response}


@socket.on('connect', namespace='/api')
def test_connect():
    print("Connected successfully")


@socket.on('message', namespace='/api')
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

    if "action" not in json_message or "target" not in json_message:
        print("Invalid request, missing action or target argument")
        return

    try:
        request_action = RequestAction(json_message["action"])
    except ValueError:
        print("Invalid action argument")
        return

    key = (request_action, json_message["target"])
    if key in request_handlers:
        print("Calling " + str(request_handlers[key]))
        request_handlers[key](json_message)
    else:
        print("Invalid request, no handler found")
