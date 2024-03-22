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

"""Provides a simple WebSocket client for debugging purposes and various other utility functions."""

import json
import logging

from websockets.sync.client import connect

logger = logging.getLogger(__name__)

def _echo_json(json_string):
    """Prints a JSON string in a human-readable format.

    Args:
        json_string (str): The JSON string to be pretty-printed.

    """

    try:
        from rich.console import Console
        console = Console()

        console.print_json(json_string)
        console.print("-" * console.size[0])
    except Exception as e:
        print(json.dumps(json_string, indent=2))
        print("-" * 80)


def get_server_status(host="127.0.0.1", port=5555):
    """Get the status of the WebSocket server.

    Args:
        host (str): The hostname or IP address of the WebSocket server. Defaults to ``127.0.0.1``.
        port (int): The port number of the WebSocket server. Defaults to ``5555``.

    Returns:
        dict: A dictionary containing the status of the WebSocket server. If the server is running,
              it returns {"status": "RUNNING"}. If the server is not running, it returns {"status": "UNKNOWN"}.

    """

    try:
        websocket = connect(f"ws://{host}:{port}/")
        websocket.send(json.dumps({"type": "init", "client": "status"}))
        message = websocket.recv()
        return json.loads(message)
    except ConnectionRefusedError:
        logger.error("Connection refused.", exc_info=1)
        return {"status": "UNKNOWN"}


def is_server_running(host="127.0.0.1", port=5555):
    """Check if a WebSocket server is running.

    Args:
        host (str): The hostname or IP address of the WebSocket server. Defaults to ``127.0.0.1``.
        port (int): The port number of the WebSocket server. Defaults to ``5555``.

    Returns:
        bool: ``True`` if a WebSocket server is running, ``False`` otherwise.

    """

    json_status = get_server_status(host=host, port=port)
    return json_status["status"] == "RUNNING"


class EchoViewer:
    """WebSocket client designed for debugging purposes.

    This WebSocket client is intended for debugging purposes and is used to test WebSocket connections.
    It echoes back any received messages.

    """

    def __init__(self, host="127.0.0.1", port=5555):
        self.websocket = connect(f"ws://{host}:{port}/")
        self.websocket.send(json.dumps({"type": "init", "client": "viewer"}))

    def run(self):
        self.websocket.send(json.dumps({"type": "start"}))

        print("Waiting for reporter....")
        message = self.websocket.recv(timeout=None)
        event = json.loads(message)

        assert event["type"] == "start"

        for message in self.websocket:
            event = json.loads(message)

            _echo_json(message)

            if event["type"] == "end":
                self.websocket.close()


if __name__ == "__main__":
    client = EchoViewer()
    client.run()
