def serialize_property(prop):
    """
    Serialize a Property object into a dictionary of its attributes.

    Args:
        prop (Property): The Property model instance to be serialized.

    Returns:
        dict: A dictionary containing the essential attributes of
        the Property.
    """
    return {
        "id": prop.id,
        "lot": prop.lot,
        "section": prop.section,
        "deposited_plan": prop.deposited_plan,
        "address_street": prop.address_street,
        "address_suburb": prop.address_suburb,
        "address_state": prop.address_state,
        "address_post_code": prop.address_post_code,
    }
