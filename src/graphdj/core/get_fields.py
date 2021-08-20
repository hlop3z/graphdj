"""GraphQL - Edges & Nodes
    Get the fields requested by the client.
"""


def clean_field(node):
    """Get Edges & Nodes"""
    return_value = []
    if node.get("edges"):
        fields = node["edges"]["node"]
        for key, val in fields.items():
            if val:
                items = clean_field(val)
                return_value.extend([f"{key}.{i}" for i in items])
            else:
                return_value.append(key)
    return return_value


def find_fields(node):
    """Find all the fields in the request."""
    field = {}
    if node.selection_set:
        for leaf in node.selection_set.selections:
            if leaf.kind == "field":
                obj = {leaf.name.value: find_fields(leaf)}
                field.update(obj)
    return field


def get_fields(info):
    """Find & Clean"""
    fields = [find_fields(node) for node in info.field_nodes][0]
    return clean_field(fields)
