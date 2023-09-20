# AltWalker's LiveViewer

A web application for visualizing the progress of an AltWalker test run.

AltWalker's LiveViewer is a powerful tool designed to enhance your experience with AltWalker. This application provides real-time visualization and monitoring capabilities for your AltWalker test runs, allowing you to gain deeper insights into test execution, track progress, and identify potential issues with ease. With AltWalker's LiveViewer, you can effortlessly keep an eye on the execution of
your test models and ensure the success of your testing endeavors.

![Screenshot](https://raw.githubusercontent.com/altwalker/live-viewer/main/img/screenshot.png)

## Setup

Before you begin using AltWalker's LiveViewer, make sure you have AltWalker installed. If you haven't already, you can follow the installation instructions [here](https://altwalker.github.io/altwalker/).

Install the AltWalker LiveViewer command-line tool:

```bash
pip install altwalker-live-viewer
```

To verify that the CLI was installed correctly, run:

```bash
altwalker-viewer --version
```

You should see the version information displayed:

```bash
altwalker-viewer, version 0.4s.0
```

## Running

To use `altwalker-viewer`, you'll need the following prerequisites:

* Test model(s)
* Test code for the model(s)

If you can run your tests using `altwalker online`, you already have everything you need for the LiveViewer.

The `altwalker-viewer online` command shares arguments and options with `altwalker online`. However, it includes the `-p` option to set up the WebSocket port.

To start the WebSocket server:

```bash
altwalker-viewer online path/to/tests/ -m path/to/model.json "generator(stop_condition)" -x [python|dotnet]
```

For example:

```bash
altwalker-viewer online tests -m models/default.json "random(never)"
```

Now, open your web browser and visit: <https://altwalker.github.io/live-viewer/>.

If you want to run the frontend locally, you'll need to start a WebServer, which serves the LiveViewer frontend.

```bash
altwalker-viewer open
```

Now, open your web browser and visit: <http://localhost:8000/>.

## Troubleshooting

If you encounter any issues while using the LiveViewer, consider the following steps:

1. **Check Model and Code Validity**: First, ensure that your models and code are valid by using the following commands:

    * `altwalker check` for the model(s)
    * `altwalker verify` for code

1. **Terminating GraphWalker Processes**: If you experience problems when running the `altwalker-viewer online` command, it's essential to check for any existing GraphWalker processes. If any GraphWalker processes are running, you should stop them before running the `altwalker-viewer online` command.

## Documentation

### Getting help on commands and option names

* `-h`, `--help`: Show a help message and exit.

```bash
altwalker-viewer --help
```

```bash
altwalker-viewer online --help
```

```bash
altwalker-viewer open --help
```

## Development Setup

* python3
* node
* npm

### Install npm dependencies

```bash
npm install
```

### Install PyPi dependencies

```bash
pip install -r requirements
```

### Build the Frontend

```bash
npm run build
```

```bash
npm run start
```

### Install the CLI

```bash
pip install -e .
```

## License

This project is licensed under the [GNU General Public License v3.0](https://github.com/altwalker/live-viewer/blob/main/LICENSE).
