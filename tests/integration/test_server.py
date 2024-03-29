import json
import time

import pytest
import requests
from altwalker_viewer.__version__ import VERSION
from altwalker_viewer.cli import websocket_server
from altwalker_viewer.client import get_server_status
from altwalker_viewer.status import is_server_running
from websockets.sync.client import connect


@pytest.fixture(scope="module", autouse=True)
def test_server():
    with websocket_server() as server_process:
        while not is_server_running():
            time.sleep(0.1)

        yield server_process


def test_healthz_endpoint():
    response = requests.get("http://localhost:5555/healthz")
    assert response.status_code == 200
    assert response.text == "OK\n"

    response = requests.get("http://localhost:5555/healthz")
    assert response.status_code == 200
    assert response.text == "OK\n"


def test_versionz_endpoint():
    response = requests.get("http://localhost:5555/versionz")
    assert response.status_code == 200
    assert response.text == VERSION


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
