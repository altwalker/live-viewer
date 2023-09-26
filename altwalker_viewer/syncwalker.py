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

import traceback

import click
from altwalker.executor import create_executor
from altwalker.model import get_models
from altwalker.planner import create_planner
from altwalker.reporter import ClickReporter, Reporting
from altwalker.walker import create_walker

from .reporter import SyncWebsocketReporter


def _create_reporter(models_json):
    reporter = Reporting()
    reporter.register("click", ClickReporter())
    reporter.register("websocket", SyncWebsocketReporter(models_json=models_json))

    return reporter


def run(tests, models, executor_type, url=None, steps=None, graphwalker_port=None,
             start_element=None, unvisited=False, blocked=False):

    planner = None
    executor = None

    try:
        models_json = get_models([model for model, _ in models])

        planner = create_planner(models=models, steps=steps, port=graphwalker_port, start_element=start_element,
                                 verbose=True, unvisited=unvisited, blocked=blocked)

        executor = create_executor(executor_type, tests, url=url)
        reporter = _create_reporter(models_json)

        walker = create_walker(planner, executor, reporter=reporter)

        for _ in walker:
            planner.get_data()
    except Exception as error:
        click.secho("Test run ended with an error.")

        click.secho("\nError: ", fg="red", bold=True, nl=False)
        click.secho(str(error), fg="red")

        click.echo()
        click.secho(traceback.format_exc(), fg="red")
    finally:
        if executor:
            executor.kill()

        if planner:
            planner.kill()
