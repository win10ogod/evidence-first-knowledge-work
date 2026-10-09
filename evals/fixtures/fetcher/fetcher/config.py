"""Option resolution: flag > FETCHER_<NAME> env var > fetcher.toml [fetcher] > default."""

import os
import tomllib

DEFAULTS = {"retries": 2}
PARSERS = {"retries": int}
VALIDATORS = {"retries": (lambda v: v >= 0, "retries must be >= 0")}


class ConfigError(ValueError):
    pass


def _from_file(path):
    try:
        with open(path, "rb") as handle:
            return tomllib.load(handle).get("fetcher", {})
    except FileNotFoundError:
        return {}


def resolve(flags, environ=None, path="fetcher.toml"):
    """Return the effective options. `flags` maps option name to the CLI value or None."""
    environ = os.environ if environ is None else environ
    file_values = _from_file(path)
    options = {}
    for name, default in DEFAULTS.items():
        raw = flags.get(name)
        if raw is None:
            raw = environ.get(f"FETCHER_{name.upper()}")
        if raw is None:
            raw = file_values.get(name, default)
        try:
            value = PARSERS[name](raw)
        except (TypeError, ValueError):
            raise ConfigError(f"{name} must be a valid {PARSERS[name].__name__}") from None
        check, message = VALIDATORS[name]
        if not check(value):
            raise ConfigError(message)
        options[name] = value
    return options
