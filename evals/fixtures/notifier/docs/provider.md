# SMS provider

- The provider accepts at most **5 requests per second** per account. Requests over the limit are
  silently dropped, so the sender must stay under it.
- Sending should still go as fast as the limit allows; do not add fixed delays between messages.
- Use the vendored `throttle` package for rate limiting rather than writing a new limiter.
