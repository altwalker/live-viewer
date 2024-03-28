/*
    Copyright(C) 2023 Altom Consulting

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <https://www.gnu.org/licenses/>.
*/

// Models
const visualizer = new ModelVisualizer({container: "visualizer", editMode: false});;

const scale = d3.scaleLinear().range([0.3, 0.8]).domain([0, 5]).clamp(true);
const getColor = (d) => d3.interpolateYlGn(scale(d))

var oldStepId = null;
var stepCount = {}
var failedStep = {}

function displayModels(models) {
  visualizer.setModels(models);
  visualizer.repaint();
  repaintEdges();

  failedStep = {}
  stepCount = {}
}

function setGraphLayoutOptions(options) {
  const graphDirectionsMap = {
    "Top-Bottom": "TB",
    "Bottom-Top": "BT",
    "Left-Right": "LR",
    "Right-Left": "RL"
  }

  const layoutOptions = {
    rankdir: graphDirectionsMap[options.graphDirection],
    nodesep: options.vertexSeparation,
    edgesep: options.edgeSeparation,
    ranksep: options.rankSeparation,
  };

  visualizer.setGraphLayoutOptions(layoutOptions);
}

function repaintGraph() {
  visualizer.repaint();

  Object.keys(stepCount).forEach(function (id) {
    drawStep(id, false);
  });

  if (failedStep.id) {
    updateFailedStep(failedStep);
  }
}

function repaintEdges() {
  Object.keys(stepCount).forEach(function (id) {
    d3.select(`svg g#${id} path`).style("stroke", "#7f8c8d");
  });
}

function updateStep(step) {
  const id = step["id"] || null;
  const visits = stepCount[id] || 0;

  stepCount[id] = visits + 1;

  if (oldStepId) {
    drawOldStep(oldStepId);
  }

  if (id) {
    drawStep(id, true);
  }

  oldStepId = id;
}

function drawStep(id, current) {
  d3.select(`svg g#${id} rect`)
    .style("fill", getColor(stepCount[id]))
    .style("stroke", getColor(stepCount[id]));

  d3.select(`svg g#${id} path`)
    .style("stroke", getColor(stepCount[id]))

  if (current) {
    d3.select(`svg g#${id}`)
      .classed("current-node", true)
      .classed("current-edge", true);

    // Bold edges labels
    d3.selectAll("svg .edgeLabels tspan").attr("class", (d) => d.name == id ? "current-label" : "");
  }
}

function drawOldStep(id) {
  d3.select(`svg g#${id}`)
    .classed("current-node", false)
    .classed("current-edge", false);
}

function updateFailedStep(step) {
  failedStep = step;

  d3.select(`svg g#${step.id} rect`)
    .style("fill", "#c0392b")
    .style("stroke", "#c0392b");

  d3.select(`svg g#${step.id} path`)
    .style("stroke", "#c0392b")
}

window.addEventListener("resize", function() {
  repaintGraph()
});

// Create the drag bar
function createDragHandler() {
  let dragging = false;

  function dragstart(event) {
    event.preventDefault();
    dragging = true;
  }

  function dragmove(event) {
    if (dragging) {
      const percentage = (event.pageX / window.innerWidth) * 100;

      if (percentage > 30 && percentage < 70) {
        const rightPercentage = 100 - 0.05 - percentage;

        document.getElementById("left").style.width = `${percentage}%`;
        document.getElementById("right").style.width = `${rightPercentage}%`;
      }
    }
  }

  function dragend() {
    if (dragging) {
      repaintGraph();
    }

    dragging = false;
  }

  return { dragstart, dragmove, dragend };
}

document.addEventListener("DOMContentLoaded", function () {
  const dragHandler = createDragHandler();

  const dragBar = document.getElementById("drag-bar");
  dragBar.addEventListener("mousedown", dragHandler.dragstart);
  dragBar.addEventListener("touchstart", dragHandler.dragstart);

  window.addEventListener("mousemove", dragHandler.dragmove);
  window.addEventListener("touchmove", dragHandler.dragmove);
  window.addEventListener("mouseup", dragHandler.dragend);
  window.addEventListener("touchend", dragHandler.dragend);
});

// UI
const CSS_CLASSES = {
  HIDE: "d-none",
  SHOW: "show",
  BADGE: "badge",
  BADGE_DANGER: "badge-danger",
  BADGE_WARNING: "badge-warning",
  BADGE_SUCCESS: "badge-success",
};

function getPercentageClass(percentage) {
  if (percentage < 50) {
    return CSS_CLASSES.BADGE_DANGER;
  }

  if (percentage < 80) {
    return CSS_CLASSES.BADGE_WARNING;
  }

  return CSS_CLASSES.BADGE_SUCCESS;
}

function showSetupOverlay() {
  document.getElementById("setup-overlay").classList.remove(CSS_CLASSES.HIDE);
}

function hideSetupOverlay() {
  document.getElementById("setup-overlay").classList.add(CSS_CLASSES.HIDE);

  hideErrorMessage();
  hideWarningMessage();
}

function showErrorMessage(message) {
  let errorAlert = document.getElementById("error-alert");
  errorAlert.classList.remove(CSS_CLASSES.HIDE);
  errorAlert.classList.add(CSS_CLASSES.SHOW);

  document.getElementById("error-message").textContent = message;
}

function hideErrorMessage() {
  document.getElementById("error-alert").classList.add(CSS_CLASSES.HIDE);
}

function showWarningMessage(message) {
  let warningAlert = document.getElementById("warning-alert");
  warningAlert.classList.remove(CSS_CLASSES.HIDE);
  warningAlert.classList.add(CSS_CLASSES.SHOW);

  document.getElementById("warning-message").textContent = message;

  setTimeout(hideWarningMessage, 2000);
}

function hideWarningMessage() {
  document.getElementById("warning-alert").classList.add(CSS_CLASSES.HIDE);
}

function showPortError() {
  document.getElementById("port-input").classList.add("is-invalid");
}

function hidePortError() {
  document.getElementById("port-input").classList.remove("is-invalid");
}

function showCurrentStepForm() {
  document.getElementById("current-step-form").classList.remove(CSS_CLASSES.HIDE);
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
  let autoScroll = document.getElementById("auto-scroll-checkbox").checked;

  outputTextArea.value += result.output;

  if (autoScroll) {
    outputTextArea.scrollTop = outputTextArea.scrollHeight;
  }

  if (result.error) {
    updateFailedStep(result);

    document.getElementById("error-input").value = result.error.message;
    document.getElementById("trace-input").value = result.error.trace;
  }
}

function updateStatus(status) {
  let statusElement = document.getElementById("statistics-status")
  statusElement.innerText = status ? "Passed" : "Failed";
  statusElement.classList.add(CSS_CLASSES.BADGE)
  statusElement.classList.add(status ? CSS_CLASSES.BADGE_SUCCESS : CSS_CLASSES.BADGE_DANGER);
  statusElement.classList.remove(status ? CSS_CLASSES.BADGE_DANGER : CSS_CLASSES.BADGE_SUCCESS);
}

function updateStatistics(statistics) {
  document.getElementById("statistics-number-of-models").innerText = statistics.totalNumberOfModels;
  document.getElementById("statistics-completed-models").innerText = statistics.totalCompletedNumberOfModels;
  document.getElementById("statistics-failed-models").innerText = statistics.totalFailedNumberOfModels;
  document.getElementById("statistics-incomplete-models").innerText = statistics.totalIncompleteNumberOfModels;
  document.getElementById("statistics-not-executed-models").innerText = statistics.totalNotExecutedNumberOfModels;

  let edgeCoverage = document.getElementById("statistics-edge-coverage");
  edgeCoverage.innerText = `${statistics.edgeCoverage}%`;
  edgeCoverage.classList.remove(...[CSS_CLASSES.BADGE_DANGER, CSS_CLASSES.BADGE_WARNING, CSS_CLASSES.BADGE_SUCCESS]);
  edgeCoverage.classList.add(...[CSS_CLASSES.BADGE, getPercentageClass(statistics.edgeCoverage)]);

  document.getElementById("statistics-number-of-edges").innerText = statistics.totalNumberOfEdges;
  document.getElementById("statistics-visited-edges").innerText = statistics.totalNumberOfVisitedEdges;
  document.getElementById("statistics-unvisited-edges").innerText = statistics.totalNumberOfUnvisitedEdges;

  let vertexCoverage = document.getElementById("statistics-vertex-coverage");
  vertexCoverage.innerText = `${statistics.vertexCoverage}%`;
  vertexCoverage.classList.remove(...[CSS_CLASSES.BADGE_DANGER, CSS_CLASSES.BADGE_WARNING, CSS_CLASSES.BADGE_SUCCESS]);
  vertexCoverage.classList.add(...[CSS_CLASSES.BADGE, getPercentageClass(statistics.vertexCoverage)]);

  document.getElementById("statistics-number-of-vertices").innerText = statistics.totalNumberOfVertices;
  document.getElementById("statistics-visited-vertices").innerText = statistics.totalNumberOfVisitedVertices;
  document.getElementById("statistics-unvisited-vertices").innerText = statistics.totalNumberOfUnvisitedVertices;
}

function showStopButton() {
  let controls = document.getElementById("stop-run-button");
  controls.classList.add(CSS_CLASSES.SHOW);
  controls.classList.remove(CSS_CLASSES.HIDE);
}

function hideStopButton() {
  let controls = document.getElementById("stop-run-button");
  controls.classList.remove(CSS_CLASSES.SHOW);
  controls.classList.add(CSS_CLASSES.HIDE);
}

function stopRun() {
  hideStopButton();
  showSetupOverlay();
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

// WebSocket Client
function connectToWebSocket() {
  showLoadingStartButton();

  let port = document.getElementById("port-input").value;

  if (!port) {
    hideLoadingStartButton();
    showPortError();
    return;
  } else {
    hidePortError();
  }

  try {
    const ws = new WebSocket(`ws://localhost:${port}`);

    ws.onerror = (event) => {
      console.log("WebSocketError:", event);
      showSetupOverlay();
      showErrorMessage(`Could not connect to port: ${port}. Make sure the websocket server is running on the selected port.`);
    };
    ws.onopen = () => {
      ws.send(JSON.stringify({"type": "init", "client": "viewer"}));
      ws.send(JSON.stringify({"type": "start"}));
    };
    ws.onclose = () => hideLoadingStartButton();
    ws.onmessage = (event) => handleWebSocketMessage(ws, JSON.parse(event.data));
  } catch(error) {
    hideLoadingStartButton();
    showErrorMessage(`Unknown Error.`);
  }
}

const MESSAGE_TYPES = {
  START: "start",
  END: "end",
  STEP_START: "step-start",
  STEP_END: "step-end"
}

function handleWebSocketMessage(ws, message) {
  const type = message.type;

  if (type == MESSAGE_TYPES.START) {
    resetError();
    resetOutput();
    hideSetupOverlay();
    hideLoadingStartButton();

    showCurrentStepForm();
    hideStatisticsForm();

    displayModels(message.models);
  }

  if (type == MESSAGE_TYPES.STEP_START) {
    updateStep(message.step);
    updateStepStart(message.step);
  }

  if (type == MESSAGE_TYPES.STEP_END) {
    updateStepEnd(message.result);
  }

  if (type == MESSAGE_TYPES.END) {
    hideCurrentStepForm();
    showStatisticsForm();

    updateStatus(message.status);
    updateStatistics(message.statistics);

    showStopButton();

    ws.close();
  }
}

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("stop-run-button").addEventListener("click", stopRun);
  document.getElementById("settings-button").addEventListener("click", showSettingsOverlay);
  document.getElementById("save-settings-button").addEventListener("click", saveSettings);
  document.getElementById("hide-settings-button").addEventListener("click", hideSettingsOverlay);
  document.getElementById("connect-button").addEventListener("click", connectToWebSocket);
});
