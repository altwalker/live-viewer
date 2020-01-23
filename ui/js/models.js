var visualizer = new ModelVisualizer({container: "visualizer", editMode: false});;

var oldStepId = null;
var scale = d3.scaleLinear().range([0.3, 0.8]).domain([0, 5]).clamp(true);
var color = (d) => d3.interpolateYlGn(scale(d))

var count = {}

function displayModels(models) {
  console.log("Update Graph...");

  visualizer.setModels(models);
  visualizer.repaint();

  count = {}
}

function updateStep(step) {
  var id = step["id"] || null;
  var visits = count[id] || 0;

  count[id] = visits + 1;

  if (oldStepId) {
    d3.select("svg g#" + oldStepId)
      .classed("current-node", false)
      .classed("current-edge", false);
  }

  if (id) {
    d3.select("svg g#" + id + " rect")
      .style("fill", color(count[id]))
      .style("stroke", color(count[id]));

    d3.select("svg g#" + id + " path")
      .style("stroke", color(count[id]))

    d3.select("svg g#" + id)
      .classed("current-node", true)
      .classed("current-edge", true);

    // Bold edges labels
    d3.selectAll("svg .edgeLabels tspan").attr("class", (d) => d.name == id ? "current-label" : "");
  }

  oldStepId = id;
}

function updateFailedStep(step) {
  d3.select("svg g#" + step.id + " rect")
    .style("fill", "#c0392b")
    .style("stroke", "#c0392b");

  d3.select("svg g#" + step.id + " path")
    .style("stroke", "#c0392b")
}