# notifier (evaluation fixture)

Sends SMS notifications through a provider client.

```python
from notifier.send import send_all
send_all(messages, transport)   # transport(message) sends one SMS
```

Provider constraints are in [docs/provider.md](docs/provider.md). Third-party code is vendored under
`vendor/` (see each package's own files for its version and history).

## Tests

```bash
python run_tests.py
```
