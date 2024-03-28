import requests


def is_server_running(host="127.0.0.1", port=5555):
    """Check if a WebSocket server is running.

    Args:
        host (str): The hostname or IP address of the WebSocket server. Defaults to ``127.0.0.1``.
        port (int): The port number of the WebSocket server. Defaults to ``5555``.

    Returns:
        bool: ``True`` if a WebSocket server is running, ``False`` otherwise.

    """

    try:
        response = requests.get(f"http://{host}:{port}/healthz")
        return response.status_code == 200 and response.text == "OK\n"
    except requests.exceptions.ConnectionError:
        return None


def get_server_version(host="127.0.0.1", port=5555):
    """Get the version of a of the WebSocket server if one is running.

    Args:
        host (str): The hostname or IP address of the WebSocket server. Defaults to ``127.0.0.1``.
        port (int): The port number of the WebSocket server. Defaults to ``5555``.

    Returns:
        string: the version number, ``None`` if a WebSocket server is not running.

    """

    if is_server_running(host=host, port=port):
        try:
            response = requests.get(f"http://{host}:{port}/versionz")
            if response.status_code != 200:
                return None

            return response.text
        except requests.exceptions.ConnectionError:
            return None
