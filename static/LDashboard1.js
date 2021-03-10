let unreadSub = "#";
let uName = "username"
document.getElementById("unreadLab1").innerHTML = unreadSub;
document.getElementById("unreadLab2").innerHTML = "Submissions (" + unreadSub + ")";
document.getElementById("username").innerHTML = uName;

// codes for pop up settings window
const settingsModelBackground = document.querySelector(".settingmodel-background");
const settingsModel = document.querySelector(".SettingsListItem");
const settingsHidden = document.querySelector(".Settinghidden");
const closeSettingsBtn = document.querySelector(".settingmodel-close");
const modelSettings = document.querySelector(".settingmodel-mysettings");
const changed = document.querySelector(".btnChange");

document.getElementById("username2").value = uName;

function hideSettingsModel() {
    modelSettings.classList.add("Settinghidden");
    settingsModelBackground.classList.add("Settinghidden");
}
  
function showSettingsModel() {
    modelSettings.classList.remove("Settinghidden");
    settingsModelBackground.classList.remove("Settinghidden");
}

settingsModel.addEventListener("click", function () {
    showSettingsModel();
  });
closeSettingsBtn.addEventListener("click", function () {
    hideSettingsModel();
  });
settingsModelBackground.addEventListener("click", function () {
    hideSettingsModel();
  });
changed.addEventListener("click", function () {
    hideSettingsModel();
  });

//-----------------------------------------------------------------