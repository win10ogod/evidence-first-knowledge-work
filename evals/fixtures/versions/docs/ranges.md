# Version ranges

`versions.satisfies(version, range)` answers whether a version string is allowed by a range string. The
rules follow npm's range syntax; where this page and npm disagree, this page wins.

## Versions

`MAJOR.MINOR.PATCH`, optionally followed by `-PRERELEASE` and/or `+BUILD`, for example `1.4.0-rc.1+sha.5114f85`.
A leading `v` or `=` is allowed and ignored (`v1.2.3` is `1.2.3`).

Ordering follows SemVer 2.0.0 section 11:

1. Compare MAJOR, MINOR and PATCH numerically.
2. A version **with** a prerelease is lower than the same version without one (`1.0.0-rc.1 < 1.0.0`).
3. Prereleases are compared identifier by identifier (split on `.`): numeric identifiers compare
   numerically, alphanumeric ones in ASCII order, and a numeric identifier is lower than an alphanumeric
   one. If all shared identifiers are equal, the version with more identifiers is higher.
   Example chain: `1.0.0-alpha < 1.0.0-alpha.1 < 1.0.0-alpha.beta < 1.0.0-beta < 1.0.0-beta.2 < 1.0.0-beta.11 < 1.0.0-rc.1 < 1.0.0`.
4. BUILD metadata is ignored for ordering and matching (`1.0.0+a` equals `1.0.0+b`).

## Ranges

A range is one or more **comparator sets** joined by `||`. A version satisfies the range if it
satisfies any set. A comparator set is one or more comparators separated by whitespace, and a version
satisfies the set only if it satisfies every comparator in it (and the prerelease rule below).

### Primitive comparators

`<`, `<=`, `>`, `>=`, `=`, or no operator (meaning `=`), followed by a version. Whitespace between an
operator (including `~` and `^`) and its version is allowed: `>= 1.2.3` is `>=1.2.3`.

### Partial versions and X-ranges

`x`, `X` and `*` are wildcards, and missing parts count as wildcards. The empty range and `*` match any
release version.

| Range | Means |
| --- | --- |
| `*` or `""` | `>=0.0.0` |
| `1` or `1.x` | `>=1.0.0 <2.0.0-0` |
| `1.2` or `1.2.x` | `>=1.2.0 <1.3.0-0` |

### Hyphen ranges `A - B`

Inclusive on both ends. A partial `A` fills missing parts with zeros. A partial `B` accepts everything
up to the end of the part it names.

| Range | Means |
| --- | --- |
| `1.2.3 - 2.3.4` | `>=1.2.3 <=2.3.4` |
| `1.2 - 2.3.4` | `>=1.2.0 <=2.3.4` |
| `1.2.3 - 2.3` | `>=1.2.3 <2.4.0-0` |
| `1.2.3 - 2` | `>=1.2.3 <3.0.0-0` |

### Tilde `~`

Allows patch-level changes if a minor version is given, minor-level changes if not.

| Range | Means |
| --- | --- |
| `~1.2.3` | `>=1.2.3 <1.3.0-0` |
| `~1.2` | `>=1.2.0 <1.3.0-0` |
| `~1` | `>=1.0.0 <2.0.0-0` |
| `~0.2.3` | `>=0.2.3 <0.3.0-0` |
| `~1.2.3-beta.2` | `>=1.2.3-beta.2 <1.3.0-0` |

### Caret `^`

Allows changes that do not modify the left-most non-zero part.

| Range | Means |
| --- | --- |
| `^1.2.3` | `>=1.2.3 <2.0.0-0` |
| `^0.2.3` | `>=0.2.3 <0.3.0-0` |
| `^0.0.3` | `>=0.0.3 <0.0.4-0` |
| `^1.2.3-beta.2` | `>=1.2.3-beta.2 <2.0.0-0` |
| `^1.2.x` | `>=1.2.0 <2.0.0-0` |
| `^0.0.x` or `^0.0` | `>=0.0.0 <0.1.0-0` |
| `^1.x` or `^1` | `>=1.0.0 <2.0.0-0` |
| `^0.x` or `^0` | `>=0.0.0 <1.0.0-0` |

## Prerelease rule

A version that has a prerelease tag satisfies a comparator set only if **at least one comparator in that
set has a prerelease tag on the same `MAJOR.MINOR.PATCH`**. Otherwise prereleases are excluded even when
they fall inside the bounds.

- `1.2.3-alpha.7` satisfies `>1.2.3-alpha.3`: the comparator's tuple `1.2.3` matches.
- `3.4.5-alpha.9` does **not** satisfy `>1.2.3-alpha.3`, although it is higher.
- `1.2.4-beta.1` does **not** satisfy `^1.2.3`: no comparator carries a prerelease.
- `1.2.3-beta.4` satisfies `^1.2.3-beta.2`.

The `-0` in the upper bounds above is the lowest possible prerelease. It only matters for this rule's
bookkeeping: for example `2.0.0-rc.1` never satisfies `^1.2.3`.
