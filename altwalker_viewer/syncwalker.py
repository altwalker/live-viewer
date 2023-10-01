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

import json

from altwalker.exceptions import FailedTestsError, handle_errors
from altwalker.executor import create_executor
from altwalker.model import get_models
from altwalker.planner import create_planner
from altwalker.reporter import create_reporters
from altwalker.walker import create_walker

from .reporter import SyncWebsocketReporter


def _create_reporters(*args, models_json=None, **kwargs):
    reporters = create_reporters(*args, **kwargs)
    reporters.register("websocket", SyncWebsocketReporter(models_json=models_json))

    return reporters


def run(test_package, *args, executor_type=None, executor_url=None, steps=None, models=None,
        gw_host=None, gw_port=8887, start_element=None, verbose=False, unvisited=False, blocked=False,
        reporter=None, import_mode=None, **kwargs):

    reporter = reporter or create_reporters()
    planner = None
    executor = None

    try:
        planner = create_planner(models=models, steps=steps, host=gw_host, port=gw_port, start_element=start_element,
                                 verbose=verbose, unvisited=unvisited, blocked=blocked)
        executor = create_executor(executor_type, test_package, url=executor_url, import_mode=import_mode)

        walker = create_walker(planner, executor, reporter=reporter)
        walker.run()
    finally:
        if planner is not None:
            planner.kill()

        if executor is not None:
            executor.kill()

    return {
        "status": walker.status,
        "report": reporter.report()
    }


@handle_errors
def online(test_package, models, executor_type=None, executor_url=None, gw_host=None, gw_port=8887,
           start_element=None, verbose=False, unvisited=False, blocked=False, import_mode=None, **kwargs):

    models_json = get_models([model for model, _ in models])
    reporter = _create_reporters(**kwargs, models_json=models_json)
    response = run(
        test_package, models=models,
        executor_type=executor_type, executor_url=executor_url, import_mode=import_mode,
        gw_port=gw_port, gw_host=gw_host, start_element=start_element,
        verbose=verbose, unvisited=unvisited, blocked=blocked,
        reporter=reporter)

    if not response["status"]:
        raise FailedTestsError()



@handle_errors
def walk(test_package, models, steps_file, executor_type=None, executor_url=None, import_mode=None, **kwargs):
    with open(steps_file) as fp:
        steps = json.load(fp)

    models_json = get_models([model for model in models])

    reporter = _create_reporters(**kwargs, models_json=models_json)
    response = run(
        test_package,
        steps=steps,
        executor_type=executor_type,
        executor_url=executor_url,
        import_mode=import_mode,
        reporter=reporter
    )

    if not response["status"]:
        raise FailedTestsError()
