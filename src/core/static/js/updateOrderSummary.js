// Event listener for DOM content loaded
document.addEventListener("DOMContentLoaded", function () {
  // Function to update the order summary
  function updateOrderSummary() {
    let summary = "";
    let total = 0;

    // Check for selected 10.7 certificate
    const cert107 = document.querySelector(
      'input[name="certificate_10_7"]:checked'
    );
    // Check for selected 603 certificate
    const cert603 = document.querySelector(
      'input[name="certificate_603"]:checked'
    );
    const urgent107 = document.querySelector('input[name="urgent_10_7"]');
    const urgent603 = document.querySelector('input[name="urgent_603"]');

    // Add 10.7 certificate to summary if selected
    if (cert107) {
      summary += `${cert107.dataset.name}: $${cert107.dataset.price}<br>`;
      total += parseFloat(cert107.dataset.price);
      // Add urgent processing fee if selected
      if (urgent107 && urgent107.checked) {
        const fee107 = document.querySelector('span[data-fee-name*="Urgent"]');
        summary += `Urgent ${cert107.dataset.name}: $${fee107.dataset.feePrice}<br>`;
        total += parseFloat(fee107.dataset.feePrice);
      }
    }

    // Add 603 certificate to summary if selected
    if (cert603) {
      summary += `${cert603.dataset.name}: $${cert603.dataset.price}<br>`;
      total += parseFloat(cert603.dataset.price);
      // Add urgent processing fee if selected
      if (urgent603 && urgent603.checked) {
        const fee603 = document.querySelector('span[data-fee-name*="Urgent"]');
        summary += `Urgent ${cert603.dataset.name}: $${fee603.dataset.feePrice}<br>`;
        total += parseFloat(fee603.dataset.feePrice);
      }
    }

    // Add total to summary
    summary += `<strong>Total: $${total.toFixed(2)}</strong>`;

    // Update the order summary in the DOM
    const orderSummaryElement = document.getElementById("orderSummary");
    if (orderSummaryElement) {
      orderSummaryElement.innerHTML = summary;
    } else {
      console.error("orderSummary element not found");
    }
  }

  // Select all certificate inputs and urgent switches
  const certificates = document.querySelectorAll('input[name^="certificate_"]');
  const urgentSwitches = document.querySelectorAll('input[name^="urgent_"]');

  // Add event listeners to certificates and urgent switches
  certificates.forEach((cert) =>
    cert.addEventListener("change", updateOrderSummary)
  );
  urgentSwitches.forEach((urgentSwitch) =>
    urgentSwitch.addEventListener("change", updateOrderSummary)
  );

  // Initial call to set up the order summary
  updateOrderSummary();

  // Event listener for the payment button
  document
    .getElementById("paymentButton")
    .addEventListener("click", async (e) => {
      e.preventDefault();
      // Collect selected items (certificates and urgent fees)
      const selectedItems = [];

      const cert107 = document.querySelector(
        'input[name="certificate_10_7"]:checked'
      );
      const cert603 = document.querySelector(
        'input[name="certificate_603"]:checked'
      );
      const urgent107 = document.querySelector('input[name="urgent_10_7"]');
      const urgent603 = document.querySelector('input[name="urgent_603"]');

      // Add selected 10.7 certificate and urgent fee if applicable
      if (cert107) {
        selectedItems.push({
          id: cert107.value,
          name: cert107.dataset.name,
          price: parseFloat(cert107.dataset.price),
        });
        if (urgent107 && urgent107.checked) {
          const fee107 = document.querySelector(
            'span[data-fee-name*="Urgent"]'
          );
          selectedItems.push({
            id: fee107.dataset.feeId,
            name: `Urgent ${cert107.dataset.name}`,
            price: parseFloat(fee107.dataset.feePrice),
          });
        }
      }

      // Add selected 603 certificate and urgent fee if applicable
      if (cert603) {
        selectedItems.push({
          id: cert603.value,
          name: cert603.dataset.name,
          price: parseFloat(cert603.dataset.price),
        });
        if (urgent603 && urgent603.checked) {
          const fee603 = document.querySelector(
            'span[data-fee-name*="Urgent"]'
          );
          selectedItems.push({
            id: fee603.dataset.feeId,
            name: `Urgent ${cert603.dataset.name}`,
            price: parseFloat(fee603.dataset.feePrice),
          });
        }
      }

      // Send POST request to create checkout session
      const response = await fetch(createCheckoutSessionUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ selectedItems }),
      });

      // Helper function to get CSRF token from cookies
      function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
          const cookies = document.cookie.split(";");
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
              cookieValue = decodeURIComponent(
                cookie.substring(name.length + 1)
              );
              break;
            }
          }
        }
        return cookieValue;
      }

      // Handle the response from the server
      const session = await response.json();
      if (session.error) {
        console.error(session.error);
        return;
      }

      // Open Stripe checkout in a new window
      window.open(session.url, "_blank", "width=600,height=800");
    });
});
