async function loadResourcesModal() {
  const availableResource = await eel.get_available_resources()();
  const modalCustomSettingsContainer = document.getElementById(
    "modal-custom-settings-container"
  );

  for (const resource of availableResource) {
    const resourceId = resource?.id;
    const resourceTableName = resource?.table_name;
    const resourceSetting = document.createElement("div");
    resourceSetting.classList.add("CustomSettingToggle");

    const resourceSettingCheckbox = document.createElement("input");
    resourceSettingCheckbox.classList.add("CustomSettingToggleInput");
    resourceSettingCheckbox.type = "checkbox";
    resourceSettingCheckbox.id = `checkbox-${resourceId}`;
    resourceSettingCheckbox.name = resourceTableName;
    resourceSetting.appendChild(resourceSettingCheckbox);

    const resourceSettingName = document.createElement("label");
    resourceSettingName.classList.add("CustomSettingToggleLabel");
    resourceSettingName.id = `label-${resourceId}`;
    resourceSettingName.htmlFor = `checkbox-${resourceId}`;
    resourceSettingName.textContent = resource?.display_name;
    resourceSetting.appendChild(resourceSettingName);

    resourceSettingName.addEventListener("click", function () {
      resourceSettingCheckbox.checked = !resourceSettingCheckbox.checked;
    });

    modalCustomSettingsContainer.appendChild(resourceSetting);
  }
}

function openAddSettingModal() {
  const modal = document.getElementById("modal-add-setting");
  modal.style.display = "flex";
}

function closeAddSettingModal() {
  const modal = document.getElementById("modal-add-setting");
  modal.style.display = "none";
}

function getSelectedResources() {
  const selectedResources = [];
  const resourceCheckboxes = document.getElementsByClassName(
    "CustomSettingToggleInput"
  );

  for (const checkbox of resourceCheckboxes) {
    const resourceId = checkbox.id.split("-")[1];
    const resourceTableName = checkbox.name;
    const isEnabled = checkbox.checked;

    selectedResources.push({
      id: resourceId,
      table_name: resourceTableName,
      is_enabled: isEnabled,
    });
  }

  return selectedResources;
}

async function createCustomSettingFromModal() {
  const resources = getSelectedResources();
  const strategy = await getCurrentSelectedTestingStrategy();
  const strategyId = strategy?.id;
  const setting = await eel.create_resource_setting(strategyId, resources)();

  addSettingRow(setting);
  closeAddSettingModal();
}

document.addEventListener("DOMContentLoaded", function () {
  loadResourcesModal();
});
