import time
import json
import asyncio
import datetime
import functools

from altwalker.reporter import Reporter


class WebsocketReporter(Reporter):
    """This reporter sends the report through a websocket."""

    def __init__(self, websocket, delay=0.5):
        self.websocket = websocket
        self.delay = delay

    def step_start(self, step):
        asyncio.ensure_future(self.websocket.send(json.dumps({"step": step})))
        time.sleep(self.delay)

    def step_end(self, step, result):
        result["id"] = step["id"]
        result["output"] = "[{}] {}.{} - {}".format(datetime.datetime.now(), step["name"], step["modelName"], result["output"])

        asyncio.ensure_future(self.websocket.send(json.dumps({"result": result})))
        time.sleep(self.delay)