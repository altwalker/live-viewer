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

import json
import time

from websockets.sync.server import serve

CONNECTED = {
    "reporter": None,
    "viewer": None
}


def reporter_handler(websocket):
    while CONNECTED["viewer"] is None:
        time.sleep(0.1)

    try:
        for message in websocket:
            CONNECTED["viewer"].send(message)
    finally:
        CONNECTED["reporter"] = None


def viewer_handler(websocket):
    while CONNECTED["reporter"] is None:
        time.sleep(0.1)

    try:
        for message in websocket:
            CONNECTED["reporter"].send(message)
    finally:
        CONNECTED["viewer"] = None


def handler(websocket):
    print("Server started.")

    message = websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if not CONNECTED["reporter"] and event.get("client") == "reporter":
        print("Reporter connected.")

        print("")
        CONNECTED["reporter"] = websocket
        reporter_handler(websocket)

    if not CONNECTED["viewer"] and event.get("client") == "viewer":
        print("Viewer connected.")

        CONNECTED["viewer"] = websocket
        viewer_handler(websocket)

    websocket.close()


def start(host="localhost", port=5555):
    with serve(handler, host=host, port=port) as server:
        print("Starting websocket server...")
        server.serve_forever()


if __name__ == "__main__":
    start()
