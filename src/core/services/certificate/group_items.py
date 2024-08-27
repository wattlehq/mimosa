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


def build_child_parent_map(certificates):
    """
    Builds a dictionary that maps each certificate to a list of its
    parent certificates.

    Args:
        certificates (list): A list of certificates.

    Returns:
        dict: A dictionary where the keys are certificates, and the values
        are lists of the parent certificates for each key.
    """
    child_parent_map = {cert: [] for cert in certificates}
    for certificate in certificates:
        for child in certificate.child_certificates.all():
            child_parent_map[child].append(certificate)
    return child_parent_map
