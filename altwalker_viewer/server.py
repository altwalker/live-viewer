#    Copyright(C) 2023 Altom Consulting
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <https://www.gnu.org/licenses/>.

import http
import json
import logging
import time

import click
from websockets.http11 import datastructures
from websockets.sync.server import Response, serve

from .__version__ import VERSION

logger = logging.getLogger(__name__)

CONNECTED = {
    "reporter": None,
    "viewer": None
}


def health_check(websocket, request):
    if request.path == "/healthz":
        return Response(http.HTTPStatus.OK, "OK", datastructures.Headers([]), b"OK\n")
    if request.path == "/versionz":
        return Response(http.HTTPStatus.OK, "OK", datastructures.Headers([]), VERSION.encode())


def reporter_handler(websocket):
    click.secho(">>> Reporter connected.", fg='green', bold=True)

    while CONNECTED["viewer"] is None:
        time.sleep(0.1)

    try:
        for message in websocket:
            CONNECTED["viewer"].send(message)
    finally:
        CONNECTED["reporter"] = None


def viewer_handler(websocket):
    click.secho(">>> Viewer connected.", fg='green', bold=True)

    while CONNECTED["reporter"] is None:
        time.sleep(0.1)

    try:
        for message in websocket:
            CONNECTED["reporter"].send(message)
    finally:
        CONNECTED["viewer"] = None


def status_handler(websocket):
    websocket.send(json.dumps({"status": "RUNNING", "version": VERSION}))


def handler(websocket):
    # TODO: Remove after issue https://github.com/python-websockets/websockets/issues/1419 is fixed.
    if websocket.request.path in ['/healthz', '/versionz']:
        return

    message = websocket.recv()
    event = json.loads(message)

    if event.get("type") != "init":
        raise Exception(
            "Incompatible version error: The server and client versions are incompatible. "
            "Please ensure that both the server and client are using compatible versions."
        )

    if not CONNECTED["reporter"] and event.get("client") == "reporter":
        CONNECTED["reporter"] = websocket
        reporter_handler(websocket)

    if not CONNECTED["viewer"] and event.get("client") == "viewer":
        CONNECTED["viewer"] = websocket
        viewer_handler(websocket)

    if event.get("client") == "status":
        status_handler(websocket)

    websocket.close()


def start(host="localhost", port=5555):
    with serve(handler, host=host, port=port, process_request=health_check) as server:
        click.secho(f">>> Starting websocket server on port: {port}", fg='green', bold=True)
        server.serve_forever()


if __name__ == "__main__":
    start()
