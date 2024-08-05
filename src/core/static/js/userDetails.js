import { StateManager, stateKeys } from "./stateManager.js";

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("user-details-form");
  const displayDetails = document.getElementById("display-details");
  const editButton = document.getElementById("edit-details");
  const displayFullName = document.getElementById("display-full-name");
  const displayBusiness = document.getElementById("display-business");
  const inputFullName = document.getElementById("full-name");
  const inputBusiness = document.getElementById("business");

  /*
  * Display user details on page load
  */
  function displayUserDetails() {
    const userDetails = StateManager.getState("userDetails");
    if (userDetails) {
      displayFullName.textContent = userDetails.fullName;
      displayBusiness.textContent = userDetails.business;
      form.style.display = "none";
      displayDetails.style.display = "block";
    }
  }

  function showForm() {
    form.style.display = "block";
    displayDetails.style.display = "none";
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const fullName = inputFullName.value;
    const business = inputBusiness.value;

    const userDetails = { fullName, business };
    StateManager.setState(stateKeys.userDetails, userDetails);
    displayUserDetails();
  });

  editButton.addEventListener("click", showForm);

  /**
   * Clear user details when the page is refreshed
   */
  window.addEventListener("beforeunload", function () {
    StateManager.clearState(stateKeys.userDetails);
  });

  /**
   * Check if user details exist and display them
   */
  displayUserDetails();
});
