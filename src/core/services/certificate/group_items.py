def group_items_by_parent(certificates):
    """
    Groups the given certificates by their parent certificates.

    Args:
        certificates (list): A list of certificates.

    Returns:
        dict: A dictionary where the keys are certificates without parent
        certificates, and the values are lists of child certificates
        for each key.

    """
    grouped_dict = {}
    for certificate in certificates:
        if not certificate.parent_certificates.exists():
            grouped_dict[certificate] = certificate.child_certificates.all()
    return grouped_dict
