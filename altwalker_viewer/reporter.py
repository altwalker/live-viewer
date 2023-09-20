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

import asyncio
import datetime
import json

from altwalker.reporter import Reporter


class WebsocketReporter(Reporter):
    """This reporter sends the report through a websocket."""

    def __init__(self, websocket):
        self.websocket = websocket

    def step_start(self, step):
        asyncio.ensure_future(self.websocket.send(json.dumps({"step": step})))

    def step_end(self, step, result):
        result["id"] = step.get("id", None)

        if step.get("modelName", None):
            result["output"] = f"[{datetime.datetime.now()}] {step['modelName']}.{step['name']}:\n{result['output']}"
        else:
            result["output"] = f"[{datetime.datetime.now()}] {step['name']}\n{result['output']}"

        asyncio.ensure_future(self.websocket.send(json.dumps({"result": result})))
