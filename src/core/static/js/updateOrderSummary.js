document.addEventListener('DOMContentLoaded', function() {
    function updateOrderSummary() {
        console.log('updateOrderSummary called');
        let summary = "";
        let total = 0;

        const cert107 = document.querySelector('input[name="certificate_10_7"]:checked');
        const cert603 = document.querySelector('input[name="certificate_603"]:checked');
        const urgent107 = document.querySelector('input[name="urgent_10_7"]');
        const urgent603 = document.querySelector('input[name="urgent_603"]');

        if (cert107) {
            console.log('10.7 Certificate selected:', cert107.dataset.name, cert107.dataset.price);
            summary += `${cert107.dataset.name}: $${cert107.dataset.price}<br>`;
            total += parseFloat(cert107.dataset.price);
            if (urgent107 && urgent107.checked) {
                const fee107 = document.querySelector('span[data-fee-name*="Urgent"]');
                console.log('Urgent 10.7 fee:', fee107.dataset.feePrice);
                summary += `Urgent ${cert107.dataset.name}: $${fee107.dataset.feePrice}<br>`;
                total += parseFloat(fee107.dataset.feePrice);
            }
        }

        if (cert603) {
            console.log('603 Certificate selected:', cert603.dataset.name, cert603.dataset.price);
            summary += `${cert603.dataset.name}: $${cert603.dataset.price}<br>`;
            total += parseFloat(cert603.dataset.price);
            if (urgent603 && urgent603.checked) {
                const fee603 = document.querySelector('span[data-fee-name*="Urgent"]');
                console.log('Urgent 603 fee:', fee603.dataset.feePrice);
                summary += `Urgent ${cert603.dataset.name}: $${fee603.dataset.feePrice}<br>`;
                total += parseFloat(fee603.dataset.feePrice);
            }
        }

        summary += `<strong>Total: $${total.toFixed(2)}</strong>`;
        console.log('Final summary:', summary);

        const orderSummaryElement = document.getElementById('orderSummary');
        if (orderSummaryElement) {
            orderSummaryElement.innerHTML = summary;
        } else {
            console.error('orderSummary element not found');
        }
    }

    const certificates = document.querySelectorAll('input[name^="certificate_"]');
    const urgentSwitches = document.querySelectorAll('input[name^="urgent_"]');

    certificates.forEach(cert => cert.addEventListener('change', updateOrderSummary));
    urgentSwitches.forEach(urgentSwitch => urgentSwitch.addEventListener('change', updateOrderSummary));

    updateOrderSummary(); // Initial call to set up the order summary

    document.getElementById('paymentButton').addEventListener('click', async (e) => {
        e.preventDefault();
        const selectedItems = [];
        
        const cert107 = document.querySelector('input[name="certificate_10_7"]:checked');
        const cert603 = document.querySelector('input[name="certificate_603"]:checked');
        const urgent107 = document.querySelector('input[name="urgent_10_7"]');
        const urgent603 = document.querySelector('input[name="urgent_603"]');

        if (cert107) {
            selectedItems.push({
                id: cert107.value,
                name: cert107.dataset.name,
                price: parseFloat(cert107.dataset.price)
            });
            if (urgent107 && urgent107.checked) {
                const fee107 = document.querySelector('span[data-fee-name*="Urgent"]');
                selectedItems.push({
                    id: fee107.dataset.feeId,
                    name: `Urgent ${cert107.dataset.name}`,
                    price: parseFloat(fee107.dataset.feePrice)
                });
            }
        }

        if (cert603) {
            selectedItems.push({
                id: cert603.value,
                name: cert603.dataset.name,
                price: parseFloat(cert603.dataset.price)
            });
            if (urgent603 && urgent603.checked) {
                const fee603 = document.querySelector('span[data-fee-name*="Urgent"]');
                selectedItems.push({
                    id: fee603.dataset.feeId,
                    name: `Urgent ${cert603.dataset.name}`,
                    price: parseFloat(fee603.dataset.feePrice)
                });
            }
        }

        console.log('Selected items:', selectedItems);

        const response = await fetch(createCheckoutSessionUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')

            },
            body: JSON.stringify({ selectedItems })
        });

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        const session = await response.json();
        if (session.error) {
            console.error(session.error);
            return;
        }

        window.open(session.url, '_blank', 'width=600,height=800');
    });
});
