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

import http.server
import json
import logging
import os
import pathlib
import warnings
from contextlib import contextmanager
from multiprocessing import Process

import click
from altwalker.executor import get_supported_executors
from altwalker.generate import get_supported_languages
from altwalker.loader import get_supported_loaders

from . import syncwalker
from .__version__ import VERSION
from .client import is_server_running
from .syncserver import start

CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


model_and_generator_option = click.option(
    "--model", "-m", "models", type=(click.Path(exists=True, dir_okay=False), str),
    required=True, multiple=True,
    help="The model as a graphml/json file followed by a generator with a stop condition.")

model_file_option = click.option(
    "--model", "-m", "model_paths", type=click.Path(exists=True, dir_okay=False),
    required=True, multiple=True,
    help="The model as a graphml/json file.")


start_element_option = click.option(
    "--start-element", "-e",
    help="Sets the starting element in the first model.")

verbose_option = click.option(
    "--verbose", "-o", default=False, show_default=True, is_flag=True,
    help="Will also print the model data and the properties for each step.")

unvisited_option = click.option(
    "--unvisited", "-u", default=False, show_default=True, is_flag=True,
    help="Will also print the remaining unvisited elements in the model.")

blocked_option = click.option(
    "--blocked", "-b", default=False, show_default=True, is_flag=True,
    help="Will filter out elements with the blocked property.")

language_option = click.option(
    "--language", "-l", type=click.Choice(get_supported_languages(), case_sensitive=False),
    help="Configure the programming language of the tests.")

executor_option = click.option(
    "--executor", "-x", "--language", "-l", "executor_type",
    type=click.Choice(get_supported_executors(), case_sensitive=False),
    default="python", show_default=True,
    help="Configure the executor to be used.")

executor_url_option = click.option(
    "--executor-url", help="Sets the url for the executor.")

import_mode_option = click.option(
    "--import-mode", "import_mode",
    type=click.Choice(get_supported_loaders(), case_sensitive=False),
    default="importlib", show_default=True, envvar="ALTWALKER_IMPORT_MODE",
    help="Sets the importing mode for the Python language, which controls how modules are loaded and executed."
)


graphwalker_host_option = click.option(
    "--gw-host",
    help="Sets the host of the GraphWalker REST service.")

graphwalker_port_option = click.option(
    "--gw-port", default=8887, show_default=True,
    help="Sets the port of the GraphWalker REST service.")


report_file_option = click.option(
    "--report-file", type=click.Path(exists=False, dir_okay=False),
    help="Save the report in a file.")

report_path_option = click.option(
    "--report-path", default=False, is_flag=True,
    help="Report the execution path and save it into a file (path.json by default).")

report_path_file_option = click.option(
    "--report-path-file", type=click.Path(exists=False, dir_okay=False),
    help="Set the report path file.")

report_xml_option = click.option(
    "--report-xml", default=False, is_flag=True,
    help="Report the execution path and save it into a file (report.xml by default).")

report_xml_file_option = click.option(
    "--report-xml-file", type=click.Path(exists=False, dir_okay=False),
    help="Set the xml report file.")


def click_formatwarning(message, category, filename, lineno, file=None, line=None):
    """Format a warning on a single line and style the text."""

    return click.style("{}: {}\n".format(category.__name__, message), fg="yellow")


warnings.formatwarning = click_formatwarning


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


@contextmanager
def websocket_server(host="127.0.0.1", port=5555):
    """Context manager to ensure a WebSocket server is running and close it when done."""

    server_process = None
    if not is_server_running(host, port):
        server_process = Process(target=start, args=(host, port))
        server_process.start()

    yield server_process

    if server_process is not None:
        server_process.terminate()
        server_process.join()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(VERSION , "-v", "--version", prog_name="altwalker-viewer")
@click.option("--log-level",
              type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"], case_sensitive=False),
              default=None, show_default=True, envvar="ALTWALKER_LOG_LEVEL",
              help="Sets the logger level to the specified level.")
@click.option("--log-file", type=click.Path(exists=False, dir_okay=False), envvar="ALTWALKER_LOG_FILE",
              help="Sends logging output to a file.")
def cli(log_level=None, log_file=None):
    """A command-line tool for starting the live viewer."""

    logger = logging.getLogger(__package__)

    if log_level:
        logger.setLevel(log_level.upper())

    if log_file:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(filename=log_file)
        handler.setFormatter(formatter)
        logger.addHandler(handler)


@cli.command()
@click.option("--host", "-h", "host", default="localhost", help="Set the binding host for the WebSocket server.", show_default=True)
@click.option("--port", "-p", "port", default=5555, help="Set the port for the WebSocket server.", show_default=True)
def serve(host, port):
    """Starts the WebSocket server."""

    start(host=host, port=port)


@cli.command()
@click.argument("test_package", type=click.Path(exists=True))
@click.option("--host", "-h", "host", default="localhost", help="Set the binding host for the WebSocket server.", show_default=True)
@click.option("--port", "-p", "port", default=5555, help="Set the port for the WebSocket server.", show_default=True)
@add_options([graphwalker_host_option, graphwalker_port_option,
              model_and_generator_option, start_element_option, executor_option, executor_url_option,
              verbose_option, unvisited_option, blocked_option,
              report_path_option, report_path_file_option, report_file_option,
              report_xml_option, report_xml_file_option, import_mode_option])
def online(test_package, models, port, host, **options):
    """Starts the websocket server for an online run."""

    with websocket_server(host=host, port=port):
        syncwalker.online(test_package, models, **options)


@cli.command()
@click.argument("test_package", type=click.Path(exists=True))
@click.argument("steps_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--host", "-h", "host", default="localhost", help="Set the binding host for the WebSocket server.", show_default=True)
@click.option("--port", "-p", "port", default=5555, help="Set the port for the WebSocket server.", show_default=True)
@add_options([executor_option, executor_url_option, import_mode_option,
              report_path_option, report_path_file_option, report_file_option,
              report_xml_option, report_xml_file_option])
def walk(test_package, steps_path, host, port, **options):
    """Starts the websocket server for a walk."""

    with open(steps_path) as f:
        steps = json.load(f)

    with websocket_server(host=host, port=port):
        syncwalker.walk(test_package, steps, **options)


@cli.command("open")
@click.option("--host", "-h", "host", default="localhost", help="Set the binding host for the HTTP server.", show_default=True)
@click.option("--port", "-p", "port", default=5555, help="Set the port for the HTTP server.", show_default=True)
def open_frontend(host, port):
    """Starts a web server for the html page."""

    click.secho("Starting the web server...", fg='green', bold=True)
    click.secho("Visit: ", fg='green', bold=True, nl=False)
    click.echo("http://localhost:8000")

    path = pathlib.Path(__file__).parent
    view_path = pathlib.Path("./dist")
    os.chdir(path.joinpath(view_path).resolve())

    server_address = (host, port)
    httpd = http.server.HTTPServer(server_address, http.server.CGIHTTPRequestHandler)
    httpd.serve_forever()
