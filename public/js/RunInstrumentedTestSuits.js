const socketUrl = "ws://localhost:8765";

async function getExecutionParameters() {
  return await eel.get_execution_parameters()();
}

async function getStrategyWithSelectedSettings() {
  const strategy = await getCurrentSelectedTestingStrategy();
  const selectedSettings = getCurrentlySelectedSettings();

  const selectedSettingsWithResources = await strategy.settings.reduce(
    (acc, setting) => {
      const selectedSetting = selectedSettings.find(
        (selectedSetting) => selectedSetting.id == setting.id
      );

      if (selectedSetting) {
        acc.push(setting);
      }

      return acc;
    },
    []
  );

  const strategyWithSelectedSettings = {
    ...strategy,
    settings: selectedSettingsWithResources,
  };

  return strategyWithSelectedSettings;
}

function instrumentedTestsButtonsController() {
  const runTestsButton = document.getElementById("run-tests-button");
  const abortTestsButton = document.getElementById("abort-tests-button");

  function startExecution() {
    runTestsButton.style.display = "none";
    abortTestsButton.style.display = "block";
  }

  function stopExecution() {
    runTestsButton.style.display = "block";
    abortTestsButton.style.display = "none";
  }

  return {
    startExecution,
    stopExecution,
  };
}

function progressBarController() {
  const progressBar = document.getElementById("progress-bar");

  const startProgressBar = (progressMax) => {
    progressBar.style.display = "block";
    progressBar.max = progressMax;
    progressBar.value = 0;
  };

  const updateProgressBar = (progress) => {
    progressBar.value = progress;
  };

  return {
    startProgressBar,
    updateProgressBar,
  };
}

function saveFolderPath(folderPath) {
  const viewReportsButton = document.getElementById("view-reports-button");
  viewReportsButton.style.display = "block";
  viewReportsButton.setAttribute("folder-path", folderPath);
}

function listenToSocket() {
  const socket = new WebSocket(socketUrl);

  socket.addEventListener("open", (event) => {
    console.log("[WS]: Connection established");
  });

  socket.addEventListener("close", (event) => {
    console.log("[WS]: Connection closed, reconnecting in 1s");
    setTimeout(() => {
      listenToSocket();
    }, 1000);
  });

  const sendMessage = (data) => {
    const stringifiedData = JSON.stringify(data);
    socket.send(stringifiedData);
  };

  if (socket.readyState === WebSocket.CLOSED) {
    return;
  }

  socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    const progressBar = progressBarController();
    const testsButtons = instrumentedTestsButtonsController();

    console.log("[WS]: Received data", data);

    switch (data.type) {
      case "printToTerminal":
        return appendLineToTerminal(data.payload);
      case "reportsFolderPath":
        return saveFolderPath(data.payload);
      case "startProgressBar":
        testsButtons.startExecution();
        progressBar.startProgressBar(data.payload);
        return;
      case "updateProgressBar":
        return progressBar.updateProgressBar(data.payload);
      case "finishExecution":
        testsButtons.stopExecution();
        break;
    }
  });

  const runTestsButton = document.getElementById("run-tests-button");
  runTestsButton.addEventListener("click", async () => {
    const strategy = await getStrategyWithSelectedSettings();
    const executionParameters = await getExecutionParameters();
    console.log("executionParameters", executionParameters);
    sendMessage({
      type: "runStrategyTests",
      payload: {
        execution_parameters: executionParameters,
        strategy,
      },
    });
  });
}

function appendLineToTerminal(line) {
  const terminalContainer = document.querySelector(".TerminalContainer");
  const terminalLine = document.createElement("div");
  terminalLine.classList.add("TerminalLine");
  terminalLine.innerText = `> ${line}`;
  //   terminalContainer.appendChild(terminalLine);
  // append to the top
  terminalContainer.insertBefore(terminalLine, terminalContainer.firstChild);
}

function socketAbortTests() {
  const socket = new WebSocket(socketUrl);
  socket.addEventListener("open", () => {
    socket.send(
      JSON.stringify({
        type: "abortExecution",
      })
    );
  });
}

function socketLoadEmulator() {
  const socket = new WebSocket(socketUrl);
  socket.addEventListener("open", () => {
    socket.send(
      JSON.stringify({
        type: "loadEmulator",
      })
    );
  });
}

function addEventListeners() {
  const loadEmulatorButton = document.getElementById("load-emulator-button");
  const clearTerminalButton = document.getElementById("clear-terminal-button");
  const abortTestsButton = document.getElementById("abort-tests-button");
  const viewReportsButton = document.getElementById("view-reports-button");

  loadEmulatorButton.addEventListener("click", socketLoadEmulator);
  clearTerminalButton.addEventListener("click", () => {
    const terminalContainer = document.querySelector(".TerminalContainer");
    terminalContainer.innerHTML = "";
  });
  abortTestsButton.addEventListener("click", () => {
    const message = "Are you sure you want to abort the tests?";
    openConfirmModal(message, socketAbortTests);
  });
  viewReportsButton.addEventListener("click", async () => {
    const folderPath = viewReportsButton.getAttribute("folder-path");

    if (!folderPath) {
      return;
    }

    await eel.open_folder(folderPath)();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  listenToSocket();
  addEventListeners();
});
