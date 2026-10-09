# versions (evaluation fixture)

Version parsing and range matching used by the dependency resolver.

```python
from versions import satisfies
satisfies("1.4.2", "^1.2.0")   # True
```

The range syntax is specified in [docs/ranges.md](docs/ranges.md).

## Tests

```bash
python run_tests.py
```
