import json
import enum

from . import socketio
from .plugins import list_plugins


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


def build_response(status, response):
    return json.dumps({
        "status": status,
        "response": response
    })


def get_script_list(request):
    response = []
    for script in list_plugins():
        response.append({
            "id": script.name
        })
    return build_response(ResponseStatus.Success, {"scripts": response})


request_handlers = {
    (RequestAction.Retrieve, "scriptList"): get_script_list
}


@socketio.on('message', namespace='/api')
def message_handler(message):
    print("Received: " + message)

    try:
        json_message = json.loads(message)
    except ValueError:
        print("Error parsing json")
        return

    if "action" not in json_message or "target" not in json_message:
        print("Invalid request, missing action argument")
        return

    try:
        request_action = RequestAction(json_message["action"])
    except ValueError:
        print("Error parsing action string")
        return

    key = (request_action, json_message["target"])
    if key in request_handlers:
        response = request_handlers[key](json_message)
        print("Response: " + response)
        # send response
    else:
        print("Invalid request, no handler found")

