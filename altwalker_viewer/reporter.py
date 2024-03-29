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

import datetime
import json

import click
from altwalker.reporter import Reporter
from websockets.sync.client import connect


class SyncWebsocketReporter(Reporter):
    """This reporter sends the report through a websocket."""

    def __init__(self, host="localhost", port=5555, models_json=None):
        self.host = host
        self.port = port
        self.models_json = models_json

    def start(self, message=None):
        """Report the start of a run.

        Args:
            message (:obj:`str`): A message.
        """

        self.websocket = connect(f"ws://{self.host}:{self.port}/")
        self.websocket.send(json.dumps({"type": "init", "client": "reporter"}))
        self.websocket.send(json.dumps({"type": "start", "models": self.models_json}))

        click.secho(">>> Waiting for viewer....", fg='green', bold=True)
        data = self.websocket.recv()
        event = json.loads(data)
        assert event["type"] == "start"

    def end(self, message=None, statistics=None, status=None):
        """Report the end of a run.

        Args:
            message (:obj:`str`): A message.
        """

        self.websocket.send(json.dumps({"type": "end", "statistics": statistics, "status": status}))
        self.websocket.close()

    def step_start(self, step):
        """Report the starting execution of a step.

        Args:
            step (:obj:`dict`): The step that will be executed next.
        """

        self.websocket.send(json.dumps({"type": "step-start", "step": step}))

    def step_end(self, step, result):
        """Report the result of the step execution.

        Args:
            step (:obj:`dict`): The step just executed.
            result (:obj:`dict`): The result of the step.
        """

        result["id"] = step.get("id", None)

        if step.get("modelName", None):
            result["output"] = f"[{datetime.datetime.now()}] {step['modelName']}.{step['name']}:\n{result['output']}"
        else:
            result["output"] = f"[{datetime.datetime.now()}] {step['name']}\n{result['output']}"

        self.websocket.send(json.dumps({"type": "step-end", "result": result}))

    def error(self, step, message, trace=None):
        """Report an unexpected error.

        Args:
            step (:obj:`dict`): The step executed when the error occurred.
            message (:obj:`str`): The message of the error.
            trace (:obj:`str`): The traceback.
        """

        self.websocket.send(json.dumps({"type": "error", "step": step, "message": message, "trace": trace}))
