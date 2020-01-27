import os
import pathlib
import webbrowser
import http.server

import click

from .server import start


CONTEXT_SETTINGS = dict(help_option_names=["--help", "-h"])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(None ,"-v", "--version", prog_name="LiveViewer")
def cli():
    """A command line tool for starting the live viewer."""


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
@click.option("--delay", "-d", default=0.5, help="Sets a delay between steps. (in seconds)", show_default=True)
def server(tests, models, executor, url, port, graphwalker_port, delay):
    """Starts the websocket server."""

    click.secho("Starting the websocket server on port: {}".format(port), fg='green', bold=True)
    click.secho("Waiting for a client to connect...", fg='green', bold=True)

    start(models, tests, executor, port=port, graphwalker_port=graphwalker_port, delay=delay)


@cli.command()
def open():
    """Starts a web server for the html page."""

    click.secho("Starting the web server...", fg='green', bold=True)
    click.secho("Visit: ", fg='green', bold=True, nl=False)
    click.echo("http://localhost:8000")

    path = pathlib.Path(__file__).parent
    view_path = pathlib.Path("../ui/")
    os.chdir(path.joinpath(view_path).resolve())

    server_address = ('', 8000)
    httpd = http.server.HTTPServer(server_address, http.server.CGIHTTPRequestHandler)
    httpd.serve_forever()
