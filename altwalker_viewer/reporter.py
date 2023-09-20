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
