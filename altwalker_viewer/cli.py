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
from multiprocessing import Process

import click

from .__version__ import VERSION
from .syncserver import start
from .syncwalker import run

CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


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


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(VERSION , "-v", "--version", prog_name="altwalker-viewer")
@click.option("--log-level",
              type=click.Choice(["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"], case_sensitive=False),
              default=None, show_default=True, envvar="ALTWALKER_LOG_LEVEL",
              help="Sets the logger level to the specified level.")
@click.option("--log-file", type=click.Path(exists=False, dir_okay=False), envvar="ALTWALKER_LOG_FILE",
              help="Sends logging output to a file.")
def cli(log_level, log_file):
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
@click.argument("tests", type=click.Path(exists=True))
@click.option("--model", "-m", "models",
              type=(click.Path(exists=True, dir_okay=False), str), required=True, multiple=True,
              help="The model, as a graphml/json file followed by generator with stop condition.")
@click.option("--executor", "-x", "--language", "-l", "executor", type=click.Choice(["python", "c#", "dotnet", "http"]),
              default="python", show_default=True,
              help="Configure the executor to be used.")
@click.option("--url", default="http://localhost:5000/", show_default=True,
              help="The url for the executor.")
@click.option("--port", "-p", default=5555, help="Sets the port of the websocket service.", show_default=True)
@click.option("--graphwalker-port", default=9000, help="Sets the port fo the graphwalker service.", show_default=True)
@click.option("--delay", "-d", default=0.0, help="Sets a delay between steps. (in seconds)", show_default=True)
def online(tests, models, executor, url, port, graphwalker_port, delay):
    """Starts the websocket server for an online run."""

    p = Process(target=start, args=('localhost', port))
    p.start()

    run(tests, models, executor, url=url, graphwalker_port=graphwalker_port,
             steps=None)

    p.terminate()
    p.join()


@cli.command()
@click.argument("tests", type=click.Path(exists=True))
@click.argument("steps_path", type=click.Path(exists=True, dir_okay=False))
@click.option("--model", "-m", "models",
              type=click.Path(exists=True, dir_okay=False), required=True, multiple=True,
              help="The model, as a graphml/json file followed by generator with stop condition.")
@click.option("--executor", "-x", "--language", "-l", "executor",
              type=click.Choice(["python", "c#", "dotnet", "http"]),
              default="python", show_default=True,
              help="Configure the executor to be used.")
@click.option("--url", default="http://localhost:5000/", show_default=True,
              help="The url for the executor.")
@click.option("--port", "-p", default=5555, help="Sets the port of the websocket service.", show_default=True)
@click.option("--delay", "-d", default=0.0, help="Sets a delay between steps. (in seconds)", show_default=True)
def walk(tests, models, steps_path, executor, url, port, delay):
    """Starts the websocket server for a walk."""

    with open(steps_path) as f:
        steps = json.load(f)

    models = [(model, "") for model in models]
    run(tests, models=models, executor=executor, url=url, port=port, graphwalker_port=None, delay=delay,
             steps=steps)


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
