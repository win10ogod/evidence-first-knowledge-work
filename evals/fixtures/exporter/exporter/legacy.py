"""Helpers kept for the old batch job. Not used by the command-line tool."""

import json


def export_lines(records):
    return "\n".join(json.dumps(r) for r in records)
