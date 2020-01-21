import json

from altwalker.reporter import Reporter


class WebsocketReporter(Reporter):
    """This reporter sends the report through a websocket."""

    def __init__(self, websocket):
        self.websocket = websocket

    async def step_start(self, step):
        self.websocket.send(json.dumps({"step": step}))
