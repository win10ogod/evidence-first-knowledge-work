import json


def write_json(records):
    return json.dumps(records, indent=2, sort_keys=True) + "\n"
