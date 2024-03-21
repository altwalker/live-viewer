import json

from altwalker_viewer.__version__ import VERSION
from altwalker_viewer.client import get_server_status
from websockets.sync.client import connect


def test_status():
    payload = get_server_status()
    assert payload["status"] == "RUNNING"


def test_status_version():
    payload = get_server_status()
    assert payload.get("version") == VERSION


def test_happy_flow():
    reporter_ws = connect("ws://localhost:5555/")
    reporter_ws.send(json.dumps({"type": "init", "client": "reporter"}))
    reporter_ws.send(json.dumps({"type": "start"}))

    viewer_ws = connect("ws://localhost:5555/")
    viewer_ws.send(json.dumps({"type": "init", "client": "viewer"}))
    viewer_ws.send(json.dumps({"type": "start"}))

    message = json.loads(viewer_ws.recv())
    assert message == {"type": "start"}

    expected_message = {"type": "test"}
    reporter_ws.send(json.dumps(expected_message))
    message = json.loads(viewer_ws.recv())

    assert message == expected_message

    reporter_ws.close()
    viewer_ws.close()
