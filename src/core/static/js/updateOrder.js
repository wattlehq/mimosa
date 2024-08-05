import { API } from "./api.js";
import { stateKeys, StateManager } from "./stateManager.js";

const htmlListCertificates = "#list-certificates";
const htmlListFees = "#list-fees";
const htmlOrderSummary = "#order-summary";
const htmlContinueButton = "#continue-button";

/**
 * Updates the order summary with the selected certificates and fees.
 */
function updateSummary() {
  let total = 0;
  const selectedCertificates = document.querySelectorAll(
    `${htmlListCertificates} input[type="checkbox"]:checked`
  );
  const selectedFees = document.querySelectorAll(
    `${htmlListFees} input[type="checkbox"]:checked`
  );

  selectedCertificates.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    console.debug(`Selected certificate: ${item.value}, Price: ${price}`);
    total += price;
  });

  selectedFees.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    console.debug(`Selected fee: ${item.name}, Price: ${price}`);
    total += price;
  });

  console.debug(`Total calculated: ${total}`);

  const summaryElement = document.querySelector(htmlOrderSummary);
  if (summaryElement) {
    summaryElement.textContent = `Total: ${total.toFixed(2)}`;
  }
}

/**
 * Creates an order session
 */
function createOrder() {
  const order = {};

  const selectedCertificates = Array.from(
    document.querySelectorAll(
      `${htmlListCertificates} input[type="checkbox"]:checked`
    )
  );

  const selectedFees = Array.from(
    document.querySelectorAll(`${htmlListFees} input[type="checkbox"]:checked`)
  );

  selectedCertificates.forEach(selectedCertificate => {
    const certId = parseInt(selectedCertificate.value);
    order[certId] = { certificate_id: certId, fee_id: undefined };
  });

  selectedFees.forEach(selectedFee => {
    const certId = selectedFee.dataset.certificate;
    const feeId = parseInt(selectedFee.value);
    if (certId && order[certId]) order[certId].fee_id = feeId;
  });

  const selectedProperty = StateManager.getState(stateKeys.selectedProperty);
  const propertyId = selectedProperty ? selectedProperty.id : null;

  const data = {
    property_id: propertyId,
    lines: Object.values(order)
  };

  console.debug("Data being sent to server:", data);

  /**
   * Create the order session
   */
  API.createOrderSession(data)
    .then((data) => {
      if (data.success && data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        throw new Error(data.error || "Unknown error");
      }
    })
    .catch((error) => {
      console.error("Error creating order:", error);
      alert("An error occurred while creating the order.");
    });
}

document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(
    `${htmlListCertificates} input[type="checkbox"], ${htmlListFees} input[type="checkbox"]`
  );
  checkboxes.forEach((checkbox) => {
    checkbox.addEventListener("change", updateSummary);
  });

  updateSummary();

  const continueButton = document.querySelector(htmlContinueButton);
  if (continueButton) {
    continueButton.addEventListener("click", function (event) {
      event.preventDefault();
      createOrder();
    });
  }
});
