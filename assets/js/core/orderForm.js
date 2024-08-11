const htmlContainer = ".order-form";
const htmlOrderSummary = `${htmlContainer} .order-form__totals`;
const htmlInputLines = `${htmlContainer} input[type="hidden"][name^="lines"]`;
const htmlOptionsCertificates = `${htmlContainer} input[type="checkbox"][id^="certificate"]`;
const htmlOptionsFees = `${htmlContainer} input[type="checkbox"][id^="fee"]`;

// Update totals with selected options.
function updateTotals() {
  let subtotal = 0;
  let taxTotal = 0;

  const selectedCertificates = document.querySelectorAll(
    `${htmlOptionsCertificates}:checked`
  );

  const selectedFees = document.querySelectorAll(
    `${htmlOptionsFees}:checked`
  );

  selectedCertificates.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    const taxRate = parseFloat(item.dataset.taxRate) / 100;
    const itemTax = price * taxRate;
    console.debug(`Selected certificate: ${item.value}, Price: ${price}, Tax Rate: ${taxRate}, Tax: ${itemTax}`);
    subtotal += price;
    taxTotal += itemTax;
  });

  selectedFees.forEach((item) => {
    const price = parseFloat(item.dataset.price);
    const taxRate = parseFloat(item.dataset.taxRate) / 100;
    const itemTax = price * taxRate;
    console.debug(`Selected fee: ${item.name}, Price: ${price}, Tax Rate: ${taxRate}, Tax: ${itemTax}`);
    subtotal += price;
    taxTotal += itemTax;
  });

  const total = subtotal + taxTotal;
  console.debug(`Subtotal: ${subtotal}, Tax: ${taxTotal}, Total: ${total}`);

  updateSummary(subtotal, taxTotal, total);
}

function updateSummary(subtotal, taxTotal, total) {
  const summaryElement = document.querySelector(htmlOrderSummary);
  if (summaryElement) {
    // Clear existing content
    summaryElement.textContent = '';

    // Create and append subtotal
    const subtotalElement = document.createElement('p');
    subtotalElement.textContent = `Subtotal: $${subtotal.toFixed(2)}`;
    summaryElement.appendChild(subtotalElement);

    // Create and append tax
    const taxElement = document.createElement('p');
    taxElement.textContent = `Tax: $${taxTotal.toFixed(2)}`;
    summaryElement.appendChild(taxElement);

    // Create and append total
    const totalElement = document.createElement('p');
    totalElement.textContent = `Total: $${total.toFixed(2)}`;
    summaryElement.appendChild(totalElement);
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
  linesJson.value = JSON.stringify(data);
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
