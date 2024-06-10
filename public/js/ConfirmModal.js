function openConfirmModal(message, onConfirm) {
  const modal = document.getElementById("modal-confirm");
  const confirmMessage = document.getElementById("modal-confirm-message");
  const confirmButton = document.getElementById("modal-confirm-button");
  const cancelButton = document.getElementById("modal-confirm-cancel");
  const closeButton = document.getElementById("modal-confirm-close");

  confirmMessage.textContent = message;
  modal.style.display = "flex";

  confirmButton.onclick = () => {
    onConfirm();
    closeConfirmModal();
  };
  cancelButton.onclick = closeConfirmModal;
  closeButton.onclick = closeConfirmModal;
}

function closeConfirmModal() {
  const modal = document.getElementById("modal-confirm");
  modal.style.display = "none";
}
