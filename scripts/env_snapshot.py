#!/usr/bin/env python3
"""Print a read-only snapshot of a project's environment for evidence gathering.

Reports git state, instruction files, manifests/lockfiles, available runtimes and
the installed versions of named Python distributions and Node packages. It never
imports project code, installs anything or writes files. Querying a project
virtualenv runs that interpreter in isolated mode (-I) with a short stdlib-only
snippet; site-packages .pth hooks of that environment still execute, as they do
for any interpreter start-up.

Usage (from anywhere):
    python env_snapshot.py [--root DIR] [--py DIST ...] [--node PKG ...]
                           [--python INTERPRETER] [--json]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

# Version probes are quick; anything slower usually means a hung or network-bound tool.
PROBE_TIMEOUT_SECONDS = 10
# Enough dirty paths to judge the working tree without flooding the context window.
MAX_DIRTY_LINES = 50

INSTRUCTION_FILES = ["AGENTS.md", "CLAUDE.md", "CLAUDE.local.md", "CONTRIBUTING.md", ".cursorrules"]
INSTRUCTION_GLOBS = [".claude/skills/*/SKILL.md", ".agents/skills/*/SKILL.md", ".github/copilot-instructions.md"]
MANIFESTS = [
    "pyproject.toml", "setup.cfg", "setup.py", "Pipfile", "Pipfile.lock", "poetry.lock", "uv.lock",
    "tox.ini", "noxfile.py", "pytest.ini", "package.json", "package-lock.json", "yarn.lock",
    "pnpm-lock.yaml", "bun.lockb", "bun.lock", "go.mod", "go.sum", "Cargo.toml", "Cargo.lock",
    "Gemfile", "Gemfile.lock", "pom.xml", "build.gradle", "build.gradle.kts", "composer.json",
    "Makefile", "justfile", "Dockerfile",
]
MANIFEST_GLOBS = ["requirements*.txt", ".github/workflows/*.yml", ".github/workflows/*.yaml"]
RUNTIMES = {
    "node": ["node", "--version"],
    "npm": ["npm", "--version"],
    "go": ["go", "version"],
    "cargo": ["cargo", "--version"],
    "rustc": ["rustc", "--version"],
    "java": ["java", "-version"],
}
VENV_CANDIDATES = [".venv/bin/python", "venv/bin/python", ".venv/Scripts/python.exe", "venv/Scripts/python.exe"]

# Runs inside the target interpreter: metadata lookup only, no import of the distributions.
PY_PROBE = r"""
import importlib.metadata as m, json, sys
out = {"python": sys.version.split()[0], "executable": sys.executable, "dists": {}}
for name in sys.argv[1:]:
    try:
        d = m.distribution(name)
        out["dists"][name] = {"version": d.version, "location": str(d.locate_file(""))}
    except m.PackageNotFoundError:
        out["dists"][name] = {"version": None, "error": "not installed"}
print(json.dumps(out))
"""


def run(cmd: list[str], cwd: Path) -> tuple[int | None, str]:
    """Run a read-only probe; return (exit code, combined output) without raising."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=PROBE_TIMEOUT_SECONDS,
            stdin=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        return None, "not found"
    except subprocess.TimeoutExpired:
        return None, f"timed out after {PROBE_TIMEOUT_SECONDS}s"
    except OSError as exc:
        return None, str(exc)
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def git_state(root: Path) -> dict[str, Any]:
    if shutil.which("git") is None:
        return {"available": False}
    code, top = run(["git", "rev-parse", "--show-toplevel"], root)
    if code != 0:
        return {"available": True, "repository": False}
    _, branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], root)
    _, head = run(["git", "rev-parse", "HEAD"], root)
    # --no-optional-locks keeps `status` from refreshing .git/index.
    _, status = run(["git", "--no-optional-locks", "status", "--porcelain"], root)
    dirty = [line for line in status.splitlines() if line.strip()]
    return {
        "available": True, "repository": True, "toplevel": top, "branch": branch,
        "head": head if len(head) == 40 else None, "dirty_count": len(dirty),
        "dirty": dirty[:MAX_DIRTY_LINES], "dirty_truncated": len(dirty) > MAX_DIRTY_LINES,
    }


def present(root: Path, names: list[str], globs: list[str]) -> list[str]:
    found = [name for name in names if (root / name).is_file()]
    for pattern in globs:
        found.extend(sorted(str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file()))
    return found


def python_info(root: Path, interpreter: str | None, dists: list[str]) -> dict[str, Any]:
    if interpreter is None:
        interpreter = next((str(root / c) for c in VENV_CANDIDATES if (root / c).is_file()), sys.executable)
    code, output = run([interpreter, "-I", "-c", PY_PROBE, *dists], root)
    if code != 0:
        return {"interpreter": interpreter, "error": output or f"exit {code}"}
    try:
        return json.loads(output.splitlines()[-1])
    except (ValueError, IndexError):
        return {"interpreter": interpreter, "error": f"unparseable probe output: {output[:200]}"}


def node_info(root: Path, packages: list[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name in packages:
        manifest = root / "node_modules" / name / "package.json"
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
        except FileNotFoundError:
            result[name] = {"version": None, "error": f"{manifest.relative_to(root)} not found"}
            continue
        except (OSError, ValueError) as exc:
            result[name] = {"version": None, "error": str(exc)}
            continue
        result[name] = {
            "version": data.get("version"),
            "types": data.get("types") or data.get("typings"),
            "path": str(manifest.parent),
        }
    return result


def first_version_line(output: str) -> str:
    """First meaningful line; JVMs prepend 'Picked up JAVA_TOOL_OPTIONS ...' (may hold proxy config)."""
    lines = [line for line in output.splitlines() if line.strip() and not line.startswith("Picked up ")]
    return lines[0] if lines else ""


def snapshot(root: Path, py: list[str], node: list[str], interpreter: str | None) -> dict[str, Any]:
    runtimes = {}
    for name, cmd in RUNTIMES.items():
        if shutil.which(cmd[0]):
            _, out = run(cmd, root)
            runtimes[name] = first_version_line(out)
    return {
        "root": str(root),
        "git": git_state(root),
        "instruction_files": present(root, INSTRUCTION_FILES, INSTRUCTION_GLOBS),
        "manifests": present(root, MANIFESTS, MANIFEST_GLOBS),
        "python": python_info(root, interpreter, py),
        "runtimes": runtimes,
        "node_packages": node_info(root, node) if node else {},
    }


def render(snap: dict[str, Any]) -> str:
    lines = [f"ROOT  {snap['root']}"]
    git = snap["git"]
    if git.get("repository"):
        lines.append(f"GIT   {git['branch']} @ {git['head']} | {git['dirty_count']} changed/untracked path(s)")
        lines.extend(f"      {entry}" for entry in git["dirty"])
        if git["dirty_truncated"]:
            lines.append(f"      ... first {MAX_DIRTY_LINES} shown")
    else:
        lines.append("GIT   not a repository" if git.get("available") else "GIT   git not installed")
    lines.append("RULES " + (", ".join(snap["instruction_files"]) or "none found"))
    lines.append("MANIF " + (", ".join(snap["manifests"]) or "none found"))
    py = snap["python"]
    if "error" in py:
        lines.append(f"PY    {py.get('interpreter')}: {py['error']}")
    else:
        lines.append(f"PY    {py['python']} ({py['executable']})")
        for name, info in py["dists"].items():
            if info["version"] is None:
                lines.append(f"      {name}: {info['error']}")
            else:
                lines.append(f"      {name}=={info['version']}  {info['location']}")
    for name, version in snap["runtimes"].items():
        lines.append(f"RT    {name}: {version}")
    for name, info in snap["node_packages"].items():
        if info["version"] is None and "error" in info:
            lines.append(f"NODE  {name}: {info['error']}")
            continue
        types = f" types={info['types']}" if info.get("types") else ""
        lines.append(f"NODE  {name}@{info['version']}{types}  {info['path']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="project root (default: current directory)")
    parser.add_argument("--py", action="append", default=[], metavar="DIST", help="Python distribution to report")
    parser.add_argument("--node", action="append", default=[], metavar="PKG", help="Node package to report")
    parser.add_argument("--python", metavar="INTERPRETER", help="interpreter to query (default: project venv, else this one)")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of text")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2
    snap = snapshot(root, args.py, args.node, args.python)
    print(json.dumps(snap, indent=2) if args.json else render(snap))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
