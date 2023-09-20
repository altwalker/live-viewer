import functools
import asyncio
import json
import traceback
import concurrent.futures

import click
import websockets
from altwalker.exceptions import AltWalkerException
from altwalker.planner import create_planner
from altwalker.executor import create_executor
from altwalker.model import get_models
from altwalker.reporter import ClickReporter, Reporting
from altwalker.walker import create_walker

from .reporter import WebsocketReporter


def _create_reporter(websocket):
    reporter = Reporting()
    reporter.register("click", ClickReporter())
    reporter.register("websocket", WebsocketReporter(websocket))

    return reporter


async def get_json(websocket):
    message = await websocket.recv()
    return json.loads(message)


async def walk(websocket, path, tests, models, executor_type, url=None, steps=None, graphwalker_port=None, start_element=None, unvisited=False, blocked=False, delay=0.5):
    click.secho("Client connected.\n", fg='green', bold=True)
    planner = None
    executor = None

    first_time = True
    autoplay = (await get_json(websocket)).get("autoplay", False)

    try:
        models_json = get_models([model for model, _ in models])

        planner = create_planner(models=models, steps=steps, port=graphwalker_port, start_element=start_element,
                                 verbose=True, unvisited=unvisited, blocked=blocked)
        executor = create_executor(tests, executor_type, url=url)
        reporter = _create_reporter(websocket)

        walker = create_walker(planner, executor, reporter=reporter)

        while first_time or autoplay:
            first_time = False
            await websocket.send(json.dumps({"models": models_json}))

            for _ in walker:
                await asyncio.sleep(delay)
                planner.get_data()
                await asyncio.sleep(delay)

            statistics = planner.get_statistics()
            statistics["status"] = walker.status

            await websocket.send(json.dumps({"statistics": statistics}))
            click.secho("Test run ended.")
            autoplay = (await get_json(websocket)).get("autoplay", False)

        planner.kill()

    except Exception as error:
        click.secho("Test run ended with an error.")

        click.secho("\nError: ", fg="red", bold=True, nl=False)
        click.secho(str(error), fg="red")

        click.echo()
        click.secho(traceback.format_exc(), fg="red")

        if planner:
            planner.kill()

        if executor:
            executor.kill()

    click.secho("Client disconected.", fg="yellow")
    click.secho("Waiting for a new client to connect...", fg="green")


def start(models, tests, steps=None, executor="python", url="http://localhost:5000/", port=5555, graphwalker_port=9000, delay=0.5):
    bound_walk = functools.partial(walk, tests=tests, models=models, executor_type=executor, url=url, steps=steps, graphwalker_port=graphwalker_port, start_element=None, unvisited=False, blocked=False, delay=delay)
    start_server = websockets.serve(bound_walk, 'localhost', port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()