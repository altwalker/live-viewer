import functools
import asyncio
import json
import traceback

import click
import websockets
from altwalker.exceptions import AltWalkerException
from altwalker.planner import create_planner
from altwalker.executor import create_executor
from altwalker.model import get_models
from altwalker.reporter import ClickReporter, Reporting
from altwalker.walker import create_walker

from server.reporter import WebsocketReporter


def _create_reporter(websocket):
    reporter = Reporting()
    reporter.register("click", ClickReporter())
    reporter.register("websocket", WebsocketReporter(websocket))

    return reporter


async def walk(websocket, path, models, tests, executor_type, url, graphwalker_port, delay):
    click.secho("Client connected...", fg='green', bold=True)
    planner = None
    executor = None

    try:
        models_json = get_models([model for model, _ in models])
        await websocket.send(json.dumps({"models": models_json}))

        planner = create_planner(models=models, port=graphwalker_port)
        executor = create_executor(tests, executor_type, url)
        reporter = _create_reporter(websocket)

        walker = create_walker(planner, executor, reporter=reporter)

        for step in walker:
            step["data"] = planner.get_data()

            await asyncio.sleep(delay)
            await websocket.send(json.dumps({"step": step}))

        await websocket.send(json.dumps({"staitstics": planner.get_statistics()}))
        planner.kill()
    except Exception as error:
        click.secho("\nError: ", fg="red", bold=True, nl=False)
        click.secho(str(error), fg="red")

        click.echo()
        click.secho(traceback.format_exc(), fg="red")

        if planner:
            planner.kill()

        if executor:
            executor.kill()


def start(models, tests, executor="python", url="http://localhost:5000/", port=5555, graphwalker_port=9000, delay=0.5):
    bound_walk = functools.partial(walk, models=models, tests=tests, executor_type=executor, url=url, graphwalker_port=graphwalker_port, delay=delay)
    start_server = websockets.serve(bound_walk, 'localhost', port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
