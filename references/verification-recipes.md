# Verification Recipes

Concrete commands for establishing facts quickly. Every command here is read-only **unless marked ⚠**. A ⚠ command can execute project code, write files or use the network, so treat it as an action and check its scope first.

## Contents

1. Source priority
2. Repository state
3. Python
4. Node.js / TypeScript
5. Go
6. Rust
7. CLI tools
8. Confirming that tests were actually selected
9. Online documentation

## 1. Source priority

Prefer the source that matches the version that is actually installed:

1. Installed package source, type declarations or stubs, and packaged docs for the exact installed version.
2. Official docs or source pinned to that version (a versioned docs URL, or the repository at the release tag).
3. Official "latest" docs. Use these only after confirming the behavior has not changed since the installed version (check the changelog or release notes).
4. Secondary sources, only as leads to a primary source.

Search snippets help you find a source. They do not support a claim until you open the source itself.

## 2. Repository state

```bash
python <skill-dir>/scripts/env_snapshot.py      # branch, HEAD, dirty files, manifests, instruction files, runtimes
git --no-optional-locks status --porcelain      # plain `git status` may rewrite .git/index
git diff -- <path>                              # unstaged changes to a target
git diff --cached -- <path>                     # staged changes
git log -1 --format='%H %cs' -- <path>          # last commit touching a target
git ls-files | grep -i <name>                   # tracked files by name
```

## 3. Python

```bash
python <skill-dir>/scripts/env_snapshot.py --py requests --py pydantic   # versions + location, no import
python -m pip show <dist>                       # version, location, requirements
python -c "import importlib.metadata as m; print(m.version('<dist>'))"
python -c "import importlib.util as u; print(u.find_spec('<top_level_module>').origin)"   # file to read
```

- To find a signature, read the source file located above, or any `.pyi` stub next to it or in `types-<dist>`.
- ⚠ `python -c "import inspect, mod; print(inspect.signature(mod.func))"` imports the module and runs its import-time code.
- ⚠ `python -m pydoc mod.func` also imports the module.
- Standard library: the docs are versioned per minor release (`docs.python.org/3.12/library/...`). Check "Added in version" and "Changed in version" notes against the **target** version, not just `python --version`.

**Find the target interpreter before relying on any stdlib or language feature.** The project may target an older Python than the one on PATH:

```bash
grep -n "requires-python\|python_requires" pyproject.toml setup.cfg setup.py 2>/dev/null
cat .python-version runtime.txt 2>/dev/null; grep -rn "python-version\|FROM python" .github/workflows Dockerfile 2>/dev/null
ls /usr/bin/python3* /usr/local/bin/python3* 2>/dev/null     # which interpreters exist here
python3.11 -B -c "import itertools; print(hasattr(itertools, 'batched'))"   # probe a feature on the target
```

Run the project's checks with that interpreter (for example `python3.11 -B run_tests.py`). A feature added in 3.12, such as `itertools.batched`, passes on a 3.13 PATH interpreter and fails in a 3.11 production image.

## 4. Node.js / TypeScript

```bash
cat node_modules/<pkg>/package.json             # "version", "types", "exports", "main"
npm ls <pkg>                                     # resolved version(s) in the tree
ls node_modules/<pkg>/*.d.ts node_modules/@types/<pkg> 2>/dev/null   # type declarations
```

- `node -p "require('<pkg>/package.json').version"` fails when the package's `exports` field hides `package.json`. Reading the file directly always works.
- ⚠ `npx <tool>` may download and run a package that is not installed. Prefer `./node_modules/.bin/<tool>`.

## 5. Go

```bash
go list -m all | grep <module>                  # selected module versions (may read the module cache)
go doc <pkg>.<Symbol>                           # documentation for the resolved version
go env GOMODCACHE                               # source lives under <GOMODCACHE>/<module>@<version>/
```

- ⚠ `go list`, `go doc` and `go test` may download modules when the cache is cold. Use `GOFLAGS=-mod=mod` or `-mod=readonly` according to project convention.

## 6. Rust

```bash
grep -A2 'name = "<crate>"' Cargo.lock          # locked version
ls ~/.cargo/registry/src/*/<crate>-<version>/   # exact source for that version
```

- ⚠ `cargo tree`, `cargo doc` and `cargo test` can fetch and build. Add `--offline` when the network or cache state is uncertain.

## 7. CLI tools

```bash
<tool> --version
man <tool>                                      # read before running unfamiliar flags
```

- `--help` is usually safe, but some tools treat unknown arguments as work to do, or run hooks and plugins on start-up. Read the man page or official docs first when unsure.
- Confirm that a flag exists in the **installed** version. Flags are often added, renamed or removed between releases.

## 8. Confirming that tests were actually selected

An exit code of 0 does not prove that relevant tests ran. List or verbosely run the tests and look for the specific test names.

| Runner | List or verbose | Zero-selection signals observed in real output |
| --- | --- | --- |
| unittest | `python -m unittest <module> -v` | `Ran 0 tests`, `NO TESTS RAN` (exit 5 on Python 3.12+) |
| pytest | `python -m pytest --collect-only -q` | `no tests ran`, `N deselected` with no `passed` (exit 5) |
| Jest | `./node_modules/.bin/jest --listTests` | `No tests found` (exit 1); `-t` filter: `Tests: N skipped, N total` (exit **0**) |
| Vitest | `./node_modules/.bin/vitest list` | `No test files found` (exit 1) |
| Go | `go test -list '.*' ./...` | `[no tests to run]`, `[no test files]`, `testing: warning: no tests to run` (exit **0**) |
| Cargo | `cargo test -- --list` | `running 0 tests` (exit **0**) |

The signals above were observed with Python 3.13 unittest, pytest 9.1, Jest 29.7, Vitest 2.1, Go 1.24 and Cargo 1.97. Other versions may word them differently, so confirm against your own output. A new test that does not match the runner's discovery pattern (for example `test_x.py` when the runner collects `*_test.py`) is silently ignored, while the rest of the suite passes.

The optional hook in `hooks/zero_tests_guard.py` flags these signals automatically in Claude Code.

## 9. Online documentation

- Prefer versioned URLs: `docs.python.org/3.12/`, Read the Docs `/en/<version>/`, and GitHub `tree/<tag>/` or `blob/<tag>/`.
- Record the URL, the version or date shown on the page, the section, and the claim the passage supports.
- For time-sensitive facts (prices, limits, deprecations, current releases), fetch the page during this task. Do not reuse an earlier session's reading.

**When the official docs site is unreachable**, the same text is usually in the project's repository at a release tag:

```text
https://raw.githubusercontent.com/<org>/<repo>/<tag>/<path>
  CPython docs:      .../python/cpython/v3.12.0/Doc/library/unittest.rst
  CPython changelog: .../python/cpython/v3.12.0/Misc/NEWS.d/3.12.0b1.rst
  CPython stdlib:    .../python/cpython/v3.12.0/Lib/unittest/main.py
```

Locally installed stdlib sources (`/usr/lib/python3.X/`) are version-matched evidence as well.

**"Since which version?"** Look for the changelog or release-notes entry. If there isn't one, compare the source at adjacent release tags: the last tag without the behavior and the first tag with it. Behavior can also change within a minor series (for example between x.y.1 and x.y.3), so check the patch release you name.
