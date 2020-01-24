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
  // TODO: Remove the Model-Visualizer reste the color of the edge on repaint.

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