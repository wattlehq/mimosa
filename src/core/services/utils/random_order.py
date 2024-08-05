import random

from django.db.models import Count

from core.models.certificate import Certificate
from core.models.property import Property


def generate_random_request():
    """
    Generate a random order request for testing purposes.

    Returns:
        dict: A dictionary containing 'property_id' and 'lines' keys, where
              'lines' is a list of dictionaries with 'certificate_id' and
              optionally 'fee_id'.

    Note:
        - Randomly selects a property and between 1 and all available
          certificates.
        - May include a random fee for each certificate if available.
        - Ensures that selected fees are valid for their respective
          certificates.
    """
    # Get a random property
    property_id = Property.objects.order_by("?").first().id

    # Get all certificates with their associated fees count
    certificates = Certificate.objects.annotate(fee_count=Count("fees"))

    # Randomly select between 1 and all certificates
    num_certificates = random.randint(1, certificates.count())
    selected_certificates = random.sample(list(certificates), num_certificates)

    lines = []
    for cert in selected_certificates:
        line = {"certificate_id": cert.id}

        # Randomly decide to include a fee (if the certificate has fees)
        if cert.fee_count > 0 and random.choice([True, False]):
            fee = cert.fees.order_by("?").first()
            line["fee_id"] = fee.id

        lines.append(line)

    return {"property_id": property_id, "lines": lines}
