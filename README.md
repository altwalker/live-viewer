# LiveViewer

A live viewer for an AltWalker test run.

![Screenshot](img/screenshot.png)

## Setup

> Note: You need to have AltWalker installed to use the LiveViewer.
> You can read the installig documentation [here](https://altom.gitlab.io/altwalker/altwalker/).

Clone the repo:

```
$ git clone git@gitlab.com:altom/altwalker/live-viewer.git
```

Install the command line tool:

```
$ pip install --editable .
```

Now if the cli was installed correctly you can type:

```
$ live-viewer --version
```

And you should see:

```
LiveViewer, version 0.1
```

## Running

Prerequisites:

* model(s)
* tesc code for the model(s)

> Note:
> If you can run your tests using `altwalker online` you have everything you need for the viewer.

The viewer server command shares the arguments and options with `altwalker online`, with the exception that `-p` will set the websocket port and `--graphwalker-port` will set the port for the GraphWalker service.

To start the websocket server:

```
$ live-viewer server path/to/tests/ -m path/to/model.json "generator(stop_condition)" -x [python|dotnet]
```

Example:

```
$ live-viewer server tests -m models/default.json "random(never)"
```

After you start the webscoket server you need to start a webserver.

```
$ live-viewer open
```

Now visit: http://localhost:8000/.

Or open the file from `viewer/ui/index.html`.

## Troubleshooting

If you have troubles runnig the viewer make sure that your models and code are valid.

Use:

* `altwalker check` for the model(s).
* `altwalker verify` for code.

## Documentation

### Getting help on commands and option names

* `-h`, `--help`: Show a help message and exit.

```
$ live-viewer --help
```

```
$ live-viewer server --help
```

```
$ live-viewer open --help
```

### Websocket
