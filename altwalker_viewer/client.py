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

"""Simple websocket client used for testing."""

import json

from websockets.sync.client import connect


def get_server_status(host="127.0.0.1", port=5555):
    try:
        websocket = connect(f"ws://{host}:{port}/")
        websocket.send(json.dumps({"type": "init", "client": "status"}))
        message = websocket.recv()
        return json.loads(message)
    except ConnectionRefusedError:
        return {"status": "UNKNOWN"}


def is_server_running(host="127.0.0.1", port=5555):
    json_status = get_server_status(host=host, port=port)
    return json_status["status"] == "RUNNING"


class EchoViewer:
    """Test websocket client."""

    def __init__(self, host="127.0.0.1", port=5555):
        self.websocket = connect(f"ws://{host}:{port}/")
        self.websocket.send(json.dumps({"type": "init", "client": "viewer"}))

    def start(self):
        self.websocket.send(json.dumps({"type": "start"}))

        print("Waiting for reporter....")
        message = self.websocket.recv(timeout=None)
        event = json.loads(message)

        assert event["type"] == "start"

        for message in self.websocket:
            event = json.loads(message)

            print("-" * 30)
            print(json.dumps(event, indent=2))


if __name__ == "__main__":
    client = EchoViewer()
    client.start()
