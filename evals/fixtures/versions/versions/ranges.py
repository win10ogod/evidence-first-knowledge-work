import operator
import re

from .version import Version

_OPS = {"<": operator.lt, "<=": operator.le, ">": operator.gt, ">=": operator.ge, "=": operator.eq, "": operator.eq}
_COMPARATOR = re.compile(r"^(<=|>=|<|>|=|~|\^)?\s*(.+)$")


def _expand(op, version):
    """Turn one range token into a list of (operator, Version) pairs."""
    if op == "^":
        return [(">=", version), ("<", Version(version.major + 1, 0, 0))]
    if op == "~":
        return [(">=", version), ("<", Version(version.major, version.minor + 1, 0))]
    return [(op or "", version)]


def _comparators(text):
    pairs = []
    for token in text.split():
        match = _COMPARATOR.match(token)
        if not match:
            raise ValueError(f"invalid comparator: {token!r}")
        op, raw = match.groups()
        pairs.extend(_expand(op, Version.parse(raw)))
    return pairs


def satisfies(version, range_text):
    """True if `version` is allowed by `range_text` (see docs/ranges.md)."""
    v = Version.parse(version)
    for part in range_text.split("||"):
        if all(_OPS[op](v, bound) for op, bound in _comparators(part)):
            return True
    return False
