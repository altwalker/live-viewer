import pytest
from altwalker_viewer.__version__ import VERSION
from altwalker_viewer.cli import cli, online, open_frontend, serve, walk
from click.testing import CliRunner


def test_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert f"altwalker-viewer, version {VERSION}" in result.output


@pytest.mark.parametrize('command', [cli, online, open_frontend, serve, walk])
def test_help(command):
    runner = CliRunner()
    result = runner.invoke(command, ["--help"])
    assert result.exit_code == 0
