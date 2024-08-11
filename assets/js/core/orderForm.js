import { getCookie } from './api.js';

const htmlContainer = ".order-form";
const htmlOrderSummary = `${htmlContainer} .order-form__totals`;
const htmlInputLines = `${htmlContainer} input[type="hidden"][name^="lines"]`;
const htmlOptionsCertificates = `${htmlContainer} input[type="checkbox"][id^="certificate"]`;
const htmlOptionsFees = `${htmlContainer} input[type="checkbox"][id^="fee"]`;

// Update totals with selected options.
function updateTotals() {
  let total = 0;

  const selectedCertificates = document.querySelectorAll(
    `${htmlOptionsCertificates}:checked`
  );

  const selectedFees = document.querySelectorAll(
    `${htmlOptionsFees}:checked`
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

// Update order lines with selected options.
function updateLines() {
  const order = {};

  const selectedCertificates = Array.from(
    document.querySelectorAll(
      `${htmlOptionsCertificates}:checked`
    )
  );

  const selectedFees = Array.from(
    document.querySelectorAll(`${htmlOptionsFees}:checked`)
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


  const data = Object.values(order);
  const linesJson = document.querySelector(htmlInputLines);
  if (linesJson) {
    linesJson.value = JSON.stringify(data);
  }

  validateCertificates();
}

async function validateCertificates() {
  const selectedCertificates = document.querySelectorAll(`${htmlOptionsCertificates}:checked`);
  const selectedCertificateIds = Array.from(selectedCertificates).map(cert => parseInt(cert.value));

  // Fetch the certificate bundles
  const response = await fetch('/api/get-certificate-bundles/', {
      method: 'GET',
      headers: {
          'X-CSRFToken': getCookie('csrftoken')
      }
  });

  if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
  }

  const bundles = await response.json();

  // Check if any selected certificates are redundant
  for (const bundle of bundles) {
      if (selectedCertificateIds.includes(bundle.parent_certificate) && selectedCertificateIds.includes(bundle.child_certificate)) {
          alert(`Please select either ${bundle.parent_certificate_name} or ${bundle.child_certificate_name}, but not both.`);
          selectedCertificates[selectedCertificates.length - 1].checked = false;
          updateLines();
          return;
      }
  }
}


export class OrderForm {
  constructor() {
    const optionsAll = document.querySelectorAll(
      `${htmlOptionsCertificates}, ${htmlOptionsFees}`
    );

    optionsAll.forEach((checkbox) => {
      checkbox.addEventListener("change", updateTotals);
      checkbox.addEventListener("change", updateLines);
    });

    updateTotals();
    updateLines();
  }
}
