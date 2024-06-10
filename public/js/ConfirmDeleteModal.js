function getCurrentlySelectedSettings() {
  const table = document.querySelector(".TableSettingsBody");
  const rows = table.querySelectorAll("tr");
  const selectedSettings = [];

  rows.forEach((row) => {
    const radio = row.getElementsByTagName("input")[0];
    if (radio.checked) {
      const id = row.querySelector(".TableId").textContent;
      selectedSettings.push({
        id,
      });
    }
  });

  return selectedSettings;
}

function deleteSelectedSettingsFromTable(settings) {
  const table = document.querySelector(".TableSettingsBody");

  settings.forEach((setting) => {
    const id = `row-setting-${setting.id}`;
    const row = document.getElementById(id);
    table.removeChild(row);
  });
}

async function deleteSelectedSettings() {
  const strategy = await getCurrentSelectedTestingStrategy();
  const selectedSettings = getCurrentlySelectedSettings();

  const updatedSettings = await eel.delete_testing_strategies_resource_settings(
    strategy,
    selectedSettings
  )();

  deleteSelectedSettingsFromTable(selectedSettings);
  updatedSettings.forEach((setting) => {
    const row = document.getElementById(`row-setting-${setting.previous_id}`);
    row.id = `row-setting-${setting.new_id}`;
    row.querySelector(".TableId").textContent = setting.new_id;
  });
}

function openConfirmDeleteModal() {
  const selectedSettings = getCurrentlySelectedSettings();
  if (selectedSettings.length < 1) return;

  const message = `Are you sure you want to delete ${selectedSettings.length} selected settings?`;
  openConfirmModal(message, deleteSelectedSettings);
}

document.addEventListener("DOMContentLoaded", function () {
  const deleteSelectedSettingsButton = document.getElementById(
    "delete-selected-settings-button"
  );

  deleteSelectedSettingsButton.addEventListener(
    "click",
    openConfirmDeleteModal
  );
});
