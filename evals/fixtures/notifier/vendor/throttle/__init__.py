"""throttle 2.1.0 - a small sliding-window rate limiter. See CHANGELOG.md for version history."""

import time

__version__ = "2.1.0"


class Throttle:
    """Allow at most `calls` calls in any window of `period`.

    Args:
        calls: maximum number of calls per window.
        period: window length in seconds.
        clock: returns the current time in seconds (default: time.monotonic).
        sleep: sleeps for a number of seconds (default: time.sleep).
    """

    def __init__(self, calls, period, clock=None, sleep=None):
        if calls < 1 or period <= 0:
            raise ValueError("calls must be >= 1 and period > 0")
        self.calls = calls
        self.period_ms = period
        self._clock = clock or time.monotonic
        self._sleep = sleep or time.sleep
        self._recent_ms = []

    def _now_ms(self):
        return self._clock() * 1000

    def _forget_old(self, now_ms):
        self._recent_ms = [t for t in self._recent_ms if now_ms - t < self.period_ms]

    def wait(self):
        """Block until one more call is allowed, then record it."""
        now_ms = self._now_ms()
        self._forget_old(now_ms)
        if len(self._recent_ms) >= self.calls:
            self._sleep((self.period_ms - (now_ms - self._recent_ms[0])) / 1000)
            now_ms = self._now_ms()
            self._forget_old(now_ms)
        self._recent_ms.append(now_ms)
