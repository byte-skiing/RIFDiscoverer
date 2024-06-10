async function setPreviousExecutionParameters() {
  const appProjectFolderOption = document.getElementById(
    "app-project-folder-path"
  );
  const testReportsFolderOption = document.getElementById(
    "test-reports-folder-path"
  );
  const numberOfExecutions = document.getElementById("number-of-executions");
  const gradleTaskName = document.getElementById("gradle-task-name");

  const executionParameters = await eel.get_execution_parameters()();
  const appProjectFolderPath = executionParameters.app_project_folder;
  const testReportsFolder = executionParameters.test_reports_folder;
  const numberOfExecutionsValue = executionParameters.number_of_executions;
  const gradleTaskNameValue = executionParameters.gradle_task_name;

  appProjectFolderOption.textContent = appProjectFolderPath;
  testReportsFolderOption.textContent = testReportsFolder;
  numberOfExecutions.value = numberOfExecutionsValue;
  gradleTaskName.value = gradleTaskNameValue;
}

async function selectAppProjectFolder() {
  const folderPathDisplay = document.getElementById("app-project-folder-path");
  const reportsFolderPathDisplay = document.getElementById(
    "test-reports-folder-path"
  );
  const folderPath = await eel.get_folder_os_dialog()();

  if (folderPath === null || folderPath === "") {
    return;
  }

  const reportsFolderPath = `${folderPath}/app/build/reports`;
  await eel.set_app_project_folder(folderPath)();
  await eel.set_test_reports_folder(reportsFolderPath)();
  folderPathDisplay.textContent = folderPath;
  reportsFolderPathDisplay.textContent = reportsFolderPath;
}

async function selectTestReportsFolder() {
  const folderPathDisplay = document.getElementById("test-reports-folder-path");
  const folderPath = await eel.get_folder_os_dialog()();

  if (folderPath === null || folderPath === "") {
    return;
  }

  await eel.set_test_reports_folder(folderPath)();
  folderPathDisplay.textContent = folderPath;
}

async function saveNumberOfExecutions(e) {
  const numberOfExecutionsInput = document.getElementById(
    "number-of-executions"
  );
  const numberOfExecutions = Number(e.target.value) || 1;
  const numberOfExecutionsWasSet = await eel.set_number_of_executions(
    numberOfExecutions
  )();

  if (!numberOfExecutionsWasSet) {
    numberOfExecutionsInput.style.borderColor = "red";
  } else {
    numberOfExecutionsInput.style.borderColor = "";
  }
}

function saveGradleTaskName(e) {
  const gradleTaskName = e.target.value;
  eel.set_gradle_task_name(gradleTaskName)();
}

document.addEventListener("DOMContentLoaded", async () => {
  const numberOfExecutions = document.getElementById("number-of-executions");
  const gradleTaskName = document.getElementById("gradle-task-name");

  numberOfExecutions.addEventListener("change", saveNumberOfExecutions);
  gradleTaskName.addEventListener("change", saveGradleTaskName);
});
