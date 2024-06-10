function initializeSidebar() {
  const buttons = document.getElementsByClassName("SidebarButton");

  for (let i = 0; i < buttons.length; i++) {
    buttons[i].addEventListener("click", selectScreen);
  }
}

function selectScreen(e) {
  const clickedButton = e.target;
  const selectedScreenId = clickedButton.id.replace("button", "screen");
  const selectedScreen = document.getElementById(selectedScreenId);
  const buttons = document.getElementsByClassName("SidebarButton");
  const screens = document.getElementsByClassName("MainPageScreen");

  for (let i = 0; i < buttons.length; i++) {
    buttons[i].classList.remove("SidebarButtonSelected");
  }

  for (let i = 0; i < screens.length; i++) {
    screens[i].classList.remove("MainPageSelectedScreen");
  }

  clickedButton.classList.add("SidebarButtonSelected");
  selectedScreen.classList.add("MainPageSelectedScreen");
}

document.addEventListener("DOMContentLoaded", initializeSidebar);
