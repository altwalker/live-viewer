import time

import pytest

from altwalker_viewer.cli import websocket_server
from altwalker_viewer.client import is_server_running


@pytest.fixture(scope="session", autouse=True)
def test_server():
    with websocket_server() as server_process:
        while not is_server_running():
            time.sleep(0.1)

        yield server_process
