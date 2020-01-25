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
  dragging = false;
  repaintGraph();
}

window.onload = function() {
  document.getElementById("dragbar").addEventListener("mousedown", function(e) { dragstart(e); });
  document.getElementById("dragbar").addEventListener("touchstart", function(e) { dragstart(e); });

  window.addEventListener("mousemove", function(e) { dragmove(e); });
  window.addEventListener("touchmove", function(e) { dragmove(e); });
  window.addEventListener("mouseup", dragend);
  window.addEventListener("touchend", dragend);
}