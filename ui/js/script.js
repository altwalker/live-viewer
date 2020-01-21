var port = null
var ws = null

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
  document.getElementById("port-input").classList.add("is-invalid")
}

function updateStepData(step) {
  document.getElementById("id-input").value = step.id;
  document.getElementById("name-input").value = step.name;
  document.getElementById("model-input").value = step.modelName;

  document.getElementById("data-input").value = JSON.stringify(step.data, null, '\t');
}

function uodateStatistics(statistics) {

}

function connectToWebsocket() {
  console.log("Connect to websocket...");

  port = document.getElementById("port-input").value;
  autoplay = document.getElementById("autoplay-checkbox").value;

  if (!port) {
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
      showErrorMessage(`Chould not connect to port: ${port}. Make sure the websocket server is running on the selected port.`);
    }
    ws.onopen = function(event) {
      open = true;
    };
    ws.onclose = function(event) {
      console.log("Close", event);

      if (open) {
        showSetupOverlay();
        showWarningMessage(`Websocket connection closed.`);
      }
    }
    ws.onmessage = function(event) {
      hideSetupOverlay();

      var message = JSON.parse(event.data);
      // console.log(message);

      if (message.models) {
        displayModels(message.models);
      }

      if (message.step) {
        updateStep(message.step);
        updateStepData(message.step);
      }
    }
  } catch(error) {
    showErrorMessage(`Unknow Error.`);
  }
}

window.onload = () => {
}
