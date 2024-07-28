def group_properties_by_assessment(properties):
    """
    Group properties by their assessment values.

    Args:
        properties (QuerySet): Property objects to be grouped.

    Returns:
        dict: Properties grouped by assessment.
    """
    grouped_properties = {}
    for prop in properties:
        if prop.assessment:
            if prop.assessment not in grouped_properties:
                grouped_properties[prop.assessment] = []
            grouped_properties[prop.assessment].append(prop)
    return grouped_properties
