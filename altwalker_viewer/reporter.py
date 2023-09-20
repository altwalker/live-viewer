import time
import json
import asyncio
import datetime
import functools

from altwalker.reporter import Reporter


class WebsocketReporter(Reporter):
    """This reporter sends the report through a websocket."""

    def __init__(self, websocket):
        self.websocket = websocket

    def step_start(self, step):
        asyncio.ensure_future(self.websocket.send(json.dumps({"step": step})))
        # asyncio.ensure_future(asyncio.sleep(0))

    def step_end(self, step, result):
        result["id"] = step.get("id", None)

        if step.get("modelName", None):
            result["output"] = "[{}] {}.{}:\n{}".format(datetime.datetime.now(), step["modelName"], step["name"], result["output"])
        else:
            result["output"] = "[{}] {}\n{}".format(datetime.datetime.now(), step["name"], result["output"])

        asyncio.ensure_future(self.websocket.send(json.dumps({"result": result})))
        # asyncio.ensure_future(asyncio.sleep(0))
