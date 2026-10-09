import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vendor"))


def send_all(messages, transport):
    """Send every message through `transport`; return the number sent."""
    sent = 0
    for message in messages:
        transport(message)
        sent += 1
    return sent
