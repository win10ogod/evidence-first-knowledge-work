import re

_VERSION = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$")


class Version:
    def __init__(self, major, minor, patch, prerelease=()):
        self.major, self.minor, self.patch = major, minor, patch
        self.prerelease = tuple(prerelease)

    @classmethod
    def parse(cls, text):
        match = _VERSION.match(text.strip())
        if not match:
            raise ValueError(f"invalid version: {text!r}")
        major, minor, patch, pre = match.groups()
        return cls(int(major), int(minor), int(patch), pre.split(".") if pre else ())

    def key(self):
        return (self.major, self.minor, self.patch, self.prerelease)

    def __eq__(self, other):
        return self.key() == other.key()

    def __lt__(self, other):
        return self.key() < other.key()

    def __le__(self, other):
        return self.key() <= other.key()

    def __gt__(self, other):
        return self.key() > other.key()

    def __ge__(self, other):
        return self.key() >= other.key()

    def __repr__(self):
        pre = "-" + ".".join(self.prerelease) if self.prerelease else ""
        return f"Version('{self.major}.{self.minor}.{self.patch}{pre}')"
