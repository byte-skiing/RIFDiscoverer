function handleChangeTestStrategySelector(e) {
  clearTable();
  const strategyId = e.target.value;
  selectResourceSettings(strategyId);
}

function addInterfaceEventListeners() {
  const addRandomSettingButton = document.getElementById(
    "add-random-setting-button"
  );
  const twiseRangeSelector = document.getElementById("range-selector");

  addRandomSettingButton.addEventListener("click", createRandomResourceSetting);
  twiseRangeSelector.addEventListener("change", handleChangeRangeSelector);
}

function handleChangeRangeSelector(e) {
  clearTable();

  const optionSelector = document.querySelector(
    "select.TestingStrategySelector"
  );
  const strategyName = optionSelector.value;
  const selectedRange = e.target.value;

  const rangeDisplay = document.getElementById("range-display");
  rangeDisplay.textContent = `T=${selectedRange}`;

  selectResourceSettings(strategyName);
}

async function addSelectorTestStrategies() {
  const optionSelector = document.querySelector(".TestingStrategySelector");
  const settings = await eel.get_available_settings()();

  for (const setting of settings) {
    const option = document.createElement("option");
    option.id = setting.file_name;
    option.value = setting.file_name;
    option.textContent = setting.display_name;
    optionSelector.appendChild(option);
  }

  optionSelector.addEventListener("change", handleChangeTestStrategySelector);
}

async function getCurrentSelectedTestingStrategy() {
  const settings = await eel.get_available_settings()();
  const optionSelector = document.querySelector(
    "select.TestingStrategySelector"
  );

  const strategyFileName = optionSelector?.value || settings[0]?.file_name;
  const range = getCurrentSelectedRange();
  const strategy = await eel.get_testing_strategy(strategyFileName, range)();
  return strategy;
}

async function addSettingsTableHeader() {
  const availableResource = await eel.get_available_resources()();
  const headerRow = document.querySelector(
    "tr.TableSettingsRow.TableSettingsRowHeader"
  );
  availableResource.forEach((resource) => {
    const headerCell = document.createElement("th");
    headerCell.classList.add("TableSettingsCellHeader");
    headerCell.textContent = resource?.display_name;
    headerRow.appendChild(headerCell);
  });
}

function createCheckbox(checkboxEnabled) {
  const radio = document.createElement("th");
  radio.classList.add("TableRadio");
  const input = document.createElement("input");
  input.type = "checkbox";
  input.name = "table-settings";
  input.checked = true;

  if (!checkboxEnabled) {
    input.disabled = true;
  }

  radio.appendChild(input);
  return radio;
}

function createIdCell(lineData) {
  const { id } = lineData;
  const cell = document.createElement("td");
  cell.classList.add("TableId");
  // cell.classList.add("TableSettingsCell");
  cell.textContent = id;
  return cell;
}

function handleClickCheckbox(checkbox) {
  if (checkbox.disabled) {
    return;
  }

  checkbox.checked = !checkbox.checked;
}

function addSettingRow(setting) {
  const tableBody = document.querySelector(".TableSettingsBody");
  const newRow = document.createElement("tr");
  newRow.classList.add("TableSettingsRow");
  newRow.id = `row-setting-${setting.id}`;

  const checkboxEnabled = setting?.checkbox_enabled;
  const checkboxContainer = createCheckbox(checkboxEnabled);
  const checkbox = checkboxContainer.querySelector("input");
  const idCell = createIdCell(setting);

  newRow.appendChild(checkboxContainer);
  newRow.appendChild(idCell);

  setting?.resources.forEach((resource) => {
    const resourceCell = document.createElement("td");
    resourceCell.classList.add("TableSettingsCell");
    resourceCell.textContent = resource.is_enabled ? "✓" : "✗";
    resourceCell.style.color = resource.is_enabled ? "green" : "red";
    newRow.appendChild(resourceCell);
  });

  newRow.addEventListener("click", () => handleClickCheckbox(checkbox));
  tableBody.appendChild(newRow);
}

function clearTable() {
  const tableBody = document.querySelector(".TableSettingsBody");
  tableBody.innerHTML = "";
}

function updateSelectAllSettingsCheckboxDisplay(strategy) {
  const selectAllSettingsCheckbox = document.getElementById(
    "select-all-settings"
  );

  selectAllSettingsCheckbox.checked = true;

  if (!strategy?.is_custom && !strategy?.is_random) {
    selectAllSettingsCheckbox.disabled = true;
  } else {
    selectAllSettingsCheckbox.disabled = false;
  }

  selectAllSettingsCheckbox.addEventListener("click", function () {
    const table = document.querySelector(".TableSettingsBody");
    const rows = table.querySelectorAll("tr");

    rows.forEach((row) => {
      const radio = row.getElementsByTagName("input")[0];
      radio.checked = selectAllSettingsCheckbox.checked;
    });
  });
}

function updateAddCustomSettingButtonDisplay(strategy) {
  const addCustomSettingButton = document.getElementById(
    "add-custom-setting-button"
  );

  if (strategy?.is_custom) {
    addCustomSettingButton.style.display = "block";
  } else {
    addCustomSettingButton.style.display = "none";
  }
}

function updateAddRandomSettingButtonDisplay(strategy) {
  const addRandomSettingButton = document.getElementById(
    "add-random-setting-button"
  );

  if (strategy?.is_random) {
    addRandomSettingButton.style.display = "block";
  } else {
    addRandomSettingButton.style.display = "none";
  }
}

function updateDeleteSelectedSettingsButtonDisplay(strategy) {
  const deleteSelectedSettingsButton = document.getElementById(
    "delete-selected-settings-button"
  );

  if (strategy?.is_random || strategy?.is_custom) {
    deleteSelectedSettingsButton.style.display = "block";
  } else {
    deleteSelectedSettingsButton.style.display = "none";
  }
}

function updateRangeSelectorDisplay(strategy) {
  const rangeSelector = document.getElementById("range-selector");
  rangeSelector.disabled = !strategy?.is_range_strategy;
}

async function updateStrategyDependentInterface(strategy) {
  updateSelectAllSettingsCheckboxDisplay(strategy);
  updateAddCustomSettingButtonDisplay(strategy);
  updateAddRandomSettingButtonDisplay(strategy);
  updateDeleteSelectedSettingsButtonDisplay(strategy);
  updateRangeSelectorDisplay(strategy);
}

function getCurrentSelectedRange() {
  const rangeSelector = document.getElementById("range-selector");
  return rangeSelector.value;
}

async function selectResourceSettings(strategyFileName) {
  const range = getCurrentSelectedRange();
  const strategy = await eel.get_testing_strategy(strategyFileName, range)();
  const settings = strategy?.settings;

  settings.forEach(addSettingRow);
  updateStrategyDependentInterface(strategy);
}

async function reloadResourceSettings() {
  const strategy = await getCurrentSelectedTestingStrategy();
  const strategyFileName = strategy?.file_name;
  selectResourceSettings(strategyFileName);
}

async function createRandomResourceSetting() {
  const resources = [];
  const availableResources = await eel.get_available_resources()();

  for (const resource of availableResources) {
    const isEnabled = Math.random() > 0.5;

    resources.push({
      id: resource?.id,
      table_name: resource?.table_name,
      is_enabled: isEnabled,
    });
  }

  const strategy = await getCurrentSelectedTestingStrategy();
  const strategyId = strategy?.id;
  const setting = await eel.create_resource_setting(strategyId, resources)();
  addSettingRow(setting);
}

document.addEventListener("DOMContentLoaded", function () {
  addInterfaceEventListeners();
  addSelectorTestStrategies();
  addSettingsTableHeader();
  reloadResourceSettings();
});
