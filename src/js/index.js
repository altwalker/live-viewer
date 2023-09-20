// Models
var visualizer = new ModelVisualizer({container: "visualizer", editMode: false});;

var oldStepId = null;
var scale = d3.scaleLinear().range([0.3, 0.8]).domain([0, 5]).clamp(true);
var color = (d) => d3.interpolateYlGn(scale(d))

var count = {}
var failedStep = {}

function displayModels(models) {
  console.log("Update Graph...");

  visualizer.setModels(models);
  visualizer.repaint();
  repaintEdges();

  failedStep = {}
  count = {}
}

function setGraphLayoutOptions(options) {
  console.log(options);

  const graphDirectionsMap = {
    "Top-Bottom": "TB",
    "Bottom-Top": "BT",
    "Left-Right": "LR",
    "Right-Left": "RL"
  }

  const layoutOptions = {
    "rankdir": graphDirectionsMap[options["graphDirection"]],
    "nodesep": options["vertexSeparation"],
    "edgesep": options["edgeSeparation"],
    "ranksep": options["rankSeparation"]
  }

  visualizer.setGraphLayoutOptions(layoutOptions);
}

function repaintGraph() {
  visualizer.repaint();

  Object.keys(count).forEach(function (id) {
    drawStep(id, false);
  });

  if (failedStep.id) {
    updateFailedStep(failedStep);
  }
}

function repaintEdges() {
  // TODO: Remove the Model-Visualizer reset the color of the edge on repaint.

  Object.keys(count).forEach(function (id) {
    d3.select("svg g#" + id + " path")
      .style("stroke", "#7f8c8d");
  });
}

function updateStep(step) {
  var id = step["id"] || null;
  var visits = count[id] || 0;

  count[id] = visits + 1;

  if (oldStepId) {
    drawOldStep(oldStepId);
  }

  if (id) {
    drawStep(id, true);
  }

  oldStepId = id;
}

function drawStep(id, current) {
  d3.select("svg g#" + id + " rect")
    .style("fill", color(count[id]))
    .style("stroke", color(count[id]));

  d3.select("svg g#" + id + " path")
    .style("stroke", color(count[id]))

  if (current) {
    d3.select("svg g#" + id)
    .classed("current-node", true)
    .classed("current-edge", true);

    // Bold edges labels
    d3.selectAll("svg .edgeLabels tspan").attr("class", (d) => d.name == id ? "current-label" : "");
  }
}

function drawOldStep(id) {
  d3.select("svg g#" + id)
    .classed("current-node", false)
    .classed("current-edge", false);
}

function updateFailedStep(step) {
  failedStep = step;

  d3.select("svg g#" + step.id + " rect")
    .style("fill", "#c0392b")
    .style("stroke", "#c0392b");

  d3.select("svg g#" + step.id + " path")
    .style("stroke", "#c0392b")
}

// Resize
var dragging = false;

function dragstart(event) {
  event.preventDefault();
  dragging = true;
}

function dragmove(event) {
  if (dragging) {
    var percentage = (event.pageX / window.innerWidth) * 100;

    if (percentage > 30 && percentage < 70) {
      var rightPercentage = 100 - 0.05 - percentage;

      document.getElementById("left").style.width = percentage + "%";
      document.getElementById("right").style.width = rightPercentage + "%";
    }
  }
}

function dragend() {
  if (dragging) {
    repaintGraph();
  }

  dragging = false;
}

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("dragbar").addEventListener("mousedown", function(e) { dragstart(e); });
  document.getElementById("dragbar").addEventListener("touchstart", function(e) { dragstart(e); });

  window.addEventListener("mousemove", function(e) { dragmove(e); });
  window.addEventListener("touchmove", function(e) { dragmove(e); });
  window.addEventListener("mouseup", dragend);
  window.addEventListener("touchend", dragend);
});

// Scripts

var port = null;
var ws = null;

var autoplay = false;
var maxDelay = 5;
var currentDelay = 5;

function percentageColor(percentage) {
  if (percentage < 50)
    return "badge-danger"

  if (percentage < 80)
    return "badge-warning"

  return "badge-success"
}

function showSetupOverlay() {
  document.getElementById("setup-overlay").classList.remove("d-none");
}

function hideSetupOverlay() {
  document.getElementById("setup-overlay").classList.add("d-none");

  hideErrorMessage();
  hideWarningMessage();
}

function showErrorMessage(message) {
  let errorAlert = document.getElementById("error-alert");
  errorAlert.classList.remove("d-none");
  errorAlert.classList.add("show");

  document.getElementById("error-message").textContent = message;
}

function hideErrorMessage() {
  document.getElementById("error-alert").classList.add("d-none");
}

function showWarningMessage(message) {
  let warningAlert = document.getElementById("warning-alert");
  warningAlert.classList.remove("d-none");
  warningAlert.classList.add("show");

  document.getElementById("warning-message").textContent = message;

  setTimeout(hideWarningMessage, 2000);
}

function hideWarningMessage() {
  document.getElementById("warning-alert").classList.add("d-none");
}

function showPortError() {
  document.getElementById("port-input").classList.add("is-invalid");
}

function showCurrentStepForm() {
  document.getElementById("current-step-form").classList.remove("d-none");
}

function hideCurrentStepForm() {
  document.getElementById("current-step-form").classList.add("d-none");
}

function showStatisticsForm() {
  document.getElementById("statistics-form").classList.remove("d-none");
}

function hideStatisticsForm() {
  document.getElementById("statistics-form").classList.add("d-none");
}

function showSettingsOverlay() {
  document.getElementById("settings-overlay").classList.remove("d-none");
}

function hideSettingsOverlay() {
  document.getElementById("settings-overlay").classList.add("d-none");
}

function showLoadingStartButton() {
  document.getElementById("start-button-loading").classList.remove("d-none");
  document.getElementById("start-button").classList.add("d-none");
}

function hideLoadingStartButton() {
  document.getElementById("start-button-loading").classList.add("d-none");
  document.getElementById("start-button").classList.remove("d-none");
}

function updateStepStart(step) {
  document.getElementById("id-input").value = step.id;
  document.getElementById("name-input").value = step.name;
  document.getElementById("model-input").value = step.modelName;

  if (step.data) {
    document.getElementById("data-input").value = JSON.stringify(step.data, null, '  ');
  }
}

function updateStepEnd(result) {
  let outputTextArea = document.getElementById("output-input");
  let autorscroll = document.getElementById("autoscroll-checkbox").checked;

  outputTextArea.value += result.output;

  if (autorscroll) {
    outputTextArea.scrollTop = outputTextArea.scrollHeight;
  }

  if (result.error) {
    updateFailedStep(result);

    document.getElementById("error-input").value = result.error.message;
    document.getElementById("trace-input").value = result.error.trace;
  }
}

function updateStatistics(statistics) {
  let status = document.getElementById("statistics-status")
  status.innerText = statistics.status ? "Passed" : "Failed";
  status.classList.add("badge")
  status.classList.add(statistics.status ? "badge-success" : "badge-danger");
  status.classList.remove(statistics.status ? "badge-danger" : "badge-success");


  document.getElementById("statistics-number-of-models").innerText = statistics.totalNumberOfModels;
  document.getElementById("statistics-completed-models").innerText = statistics.totalCompletedNumberOfModels;
  document.getElementById("statistics-failed-models").innerText = statistics.totalFailedNumberOfModels;
  document.getElementById("statistics-incomplete-models").innerText = statistics.totalIncompleteNumberOfModels;
  document.getElementById("statistics-not-executed-models").innerText = statistics.totalNotExecutedNumberOfModels;


  let edgeCoverage = document.getElementById("statistics-edge-coverage");
  edgeCoverage.innerText = statistics.edgeCoverage + "%";
  edgeCoverage.classList.remove(...["badge-danger", "badge-warning", "badge-success"]);
  edgeCoverage.classList.add(...["badge", percentageColor(statistics.edgeCoverage)]);

  document.getElementById("statistics-number-of-edges").innerText = statistics.totalNumberOfEdges;
  document.getElementById("statistics-visited-edges").innerText = statistics.totalNumberOfVisitedEdges;
  document.getElementById("statistics-unvisited-edges").innerText = statistics.totalNumberOfUnvisitedEdges;

  let vertexCoverage = document.getElementById("statistics-vertex-coverage");
  vertexCoverage.innerText = statistics.vertexCoverage + "%";
  vertexCoverage.classList.remove(...["badge-danger", "badge-warning", "badge-success"]);
  vertexCoverage.classList.add(...["badge", percentageColor(statistics.vertexCoverage)]);

  document.getElementById("statistics-number-of-vertices").innerText = statistics.totalNumberOfVertices;
  document.getElementById("statistics-visited-vertices").innerText = statistics.totalNumberOfVisitedVertices;
  document.getElementById("statistics-unvisited-vertices").innerText = statistics.totalNumberOfUnvisitedVertices;
}

function showAutoplayControls() {
  let controls = document.getElementById("autoplay-controls");
  controls.classList.add("d-inline-block");
  controls.classList.remove("d-none");
}

function hideAutoplayControls() {
  let controls = document.getElementById("autoplay-controls");
  controls.classList.remove("d-inline-block");
  controls.classList.add("d-none");
}

function showStopControls() {
  let controls = document.getElementById("stop-controls");
  controls.classList.add("d-inline-block");
  controls.classList.remove("d-none");
}

function hideStopControls() {
  let controls = document.getElementById("stop-controls");
  controls.classList.remove("d-inline-block");
  controls.classList.add("d-none");
}

function startCountDown(delay) {
  showAutoplayControls();
  document.getElementById("autoplay-seconds").innerText = currentDelay;

  if (currentDelay == 0) {
    ws.send(JSON.stringify({"autoplay": autoplay}));

    if (autoplay == false) {
      ws.close();
    }

    hideAutoplayControls();
    currentDelay = maxDelay;
  } else {
    setTimeout(function() {
      currentDelay = currentDelay > 0 ? currentDelay - 1 : 0;
      startCountDown();
    }, 1000);
  }
}

function skipCountDown() {
  currentDelay = 0;
}

function stopAutoplay() {
  autoplay = false;
  currentDelay = 0;
}

function stopRun() {
  hideStopControls();

  ws.send(JSON.stringify({"autoplay": autoplay}));
  ws.close();
}

function resetError() {
  document.getElementById("error-input").value = "";
  document.getElementById("trace-input").value = "";
}

function resetOutput() {
  document.getElementById("output-input").value = "";
}

function saveSettings() {
  const graphDirection = document.getElementById("graph-direction-input").value;
  const vertexSeparation = document.getElementById("vertex-separation-input").value;
  const edgeSeparation = document.getElementById("edge-separation-input").value;
  const rankSeparation = document.getElementById("rank-separation-input").value;

  setGraphLayoutOptions({
    "graphDirection": graphDirection,
    "vertexSeparation": vertexSeparation == 0 ? 50 : vertexSeparation,
    "edgeSeparation": edgeSeparation == 0 ? 50 : edgeSeparation,
    "rankSeparation": rankSeparation == 0 ? 50 : rankSeparation,
  });

  hideSettingsOverlay();
}

function connectToWebsocket() {
  console.log("Connect to websocket...");
  showLoadingStartButton();

  port = document.getElementById("port-input").value;
  autoplay = document.getElementById("autoplay-checkbox").checked;

  if (!port) {
    hideLoadingStartButton();
    showPortError();
    return
  }

  try {
    let open = false;
    let host = "localhost:" + port;
    ws = new WebSocket('ws://' + host + '/steps');

    console.log("Websocket Started.");

    ws.onerror = function(event) {
      console.log("Error", event);
      showSetupOverlay();
      showErrorMessage(`Could not connect to port: ${port}. Make sure the websocket server is running on the selected port.`);
    }
    ws.onopen = function(event) {
      ws.send(JSON.stringify({"autoplay": autoplay}));
      open = true;
    };
    ws.onclose = function(event) {
      hideLoadingStartButton();

      if (open) {
        showSetupOverlay();
        showWarningMessage(`Websocket connection closed.`);
      }
    }
    ws.onmessage = function(event) {
      var message = JSON.parse(event.data);

      if (message.models) {
        resetError();
        resetOutput();
        hideSetupOverlay();
        hideLoadingStartButton();

        showCurrentStepForm();
        hideStatisticsForm();

        displayModels(message.models);
      }

      if (message.step) {
        updateStep(message.step);
        updateStepStart(message.step);
      }

      if (message.result) {
        updateStepEnd(message.result);
      }

      if (message.statistics) {
        hideCurrentStepForm();
        showStatisticsForm();

        updateStatistics(message.statistics);
        if (autoplay) {
          startCountDown(maxDelay);
        } else {
          showStopControls();
        }
      }
    }
  } catch(error) {
    hideLoadingStartButton();
    showErrorMessage(`Unknown Error.`);
  }
}

window.addEventListener("resize", function(event) {
  repaintGraph()
});

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("stop-button").addEventListener("click", function(event) {
    stopAutoplay();
  });
  document.getElementById("skip-button").addEventListener("click", function(event) {
    skipCountDown();
  });
  document.getElementById("stop-button").addEventListener("click", function(event) {
    stopRun();
  });

  document.getElementById("settings-button").addEventListener("click", function(event) {
    showSettingsOverlay();
  });
  document.getElementById("save-settings-button").addEventListener("click", function(event) {
    saveSettings();
  });
  document.getElementById("hide-settings-button").addEventListener("click", function(event) {
    hideSettingsOverlay();
  });

  document.getElementById("connect-button").addEventListener("click", function(event) {
    connectToWebsocket();
  });
});
