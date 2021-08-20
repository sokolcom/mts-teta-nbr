import json


def get_items_mapping(filepath):
    """Decode JSON w/ items mapping"""
    mapping = {}
    with open(filepath, "r") as fp:
        mapping = json.load(fp)

    return mapping
