function initialize() {
  setPreviousExecutionParameters();
}

async function getFolderOsDialog() {
  return await eel.get_folder_os_dialog()();
}
