import urllib.request

# Tests replace this with a fake: TRANSPORT(url, timeout_ms) -> bytes.
TRANSPORT = None


def _urllib_transport(url, timeout_ms):
    with urllib.request.urlopen(url, timeout=timeout_ms / 1000) as response:
        return response.read()


class Client:
    def __init__(self, retries, timeout_ms=10_000):
        """`timeout_ms` is the per-request timeout in **milliseconds**."""
        self.retries = retries
        self.timeout_ms = timeout_ms

    def get(self, url):
        transport = TRANSPORT or _urllib_transport
        last_error = None
        for _ in range(self.retries + 1):
            try:
                return transport(url, timeout_ms=self.timeout_ms)
            except OSError as exc:
                last_error = exc
        raise last_error
