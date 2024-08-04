import { StateManager } from "./stateManager.js";

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("user-details-form");
  const displayDetails = document.getElementById("display-details");
  const editButton = document.getElementById("edit-details");

  /*
  * Display user details on page load
  */
  function displayUserDetails() {
    const userDetails = StateManager.getState("userDetails");
    if (userDetails) {
      document.getElementById("display-full-name").textContent =
        userDetails.fullName;
      document.getElementById("display-business").textContent =
        userDetails.business;
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
    const fullName = document.getElementById("full-name").value;
    const business = document.getElementById("business").value;

    const userDetails = { fullName, business };
    StateManager.setState("userDetails", userDetails);
    displayUserDetails();
  });

  editButton.addEventListener("click", showForm);

  /**
   * Clear user details when the page is refreshed
   */
  window.addEventListener("beforeunload", function () {
    StateManager.clearState("userDetails");
  });

  /**
   * Check if user details exist and display them
   */
  displayUserDetails();
});
