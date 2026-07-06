"""Load and validate YAML policy rule files.

A policy file looks like:

    rules:
      - id: SEC-001
        description: Telnet must be disabled
        severity: critical            # info | low | medium | high | critical
        groups: [all]                 # optional, default [all]
        match_absent: '^boot config flags telnetd'
      - id: SEC-010
        description: SSH must be enabled
        severity: critical
        match_present: '^boot config flags sshd'

`match_present` / `match_absent` take a single regex or a list of regexes.
Patterns are evaluated with re.MULTILINE against the raw running-config text:
every `match_present` pattern must match, no `match_absent` pattern may match.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import SEVERITIES


class PolicyError(Exception):
    """Raised when a policy file is missing or malformed."""


@dataclass(frozen=True)
class Rule:
    id: str
    description: str
    severity: str
    groups: frozenset[str]
    match_present: tuple[re.Pattern, ...]
    match_absent: tuple[re.Pattern, ...]
    source: str  # file the rule came from, for error messages


def load_policies(path: str | Path) -> list[Rule]:
    """Load all *.yml / *.yaml rule files from a directory (or a single file)."""
    path = Path(path)
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = sorted(p for p in path.iterdir() if p.suffix in (".yml", ".yaml"))
    else:
        raise PolicyError(f"policy path not found: {path}")
    if not files:
        raise PolicyError(f"no .yml/.yaml policy files found in {path}")

    rules: list[Rule] = []
    seen_ids: dict[str, str] = {}
    for file in files:
        for rule in _load_file(file):
            if rule.id in seen_ids:
                raise PolicyError(
                    f"{file}: duplicate rule id '{rule.id}' (already defined in {seen_ids[rule.id]})"
                )
            seen_ids[rule.id] = str(file)
            rules.append(rule)
    return rules


def _load_file(file: Path) -> list[Rule]:
    try:
        data = yaml.safe_load(file.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise PolicyError(f"{file}: invalid YAML: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("rules"), list):
        raise PolicyError(f"{file}: expected a top-level 'rules' list")

    rules = []
    for i, raw in enumerate(data["rules"]):
        if not isinstance(raw, dict):
            raise PolicyError(f"{file}: rule #{i + 1} is not a mapping")
        rules.append(_parse_rule(raw, file, i))
    return rules


def _parse_rule(raw: dict, file: Path, index: int) -> Rule:
    where = f"{file}: rule #{index + 1}"

    rule_id = str(raw.get("id") or "").strip()
    if not rule_id:
        raise PolicyError(f"{where}: 'id' is required")
    where = f"{file}: rule '{rule_id}'"

    description = str(raw.get("description") or "").strip()
    if not description:
        raise PolicyError(f"{where}: 'description' is required")

    severity = str(raw.get("severity") or "").strip().lower()
    if severity not in SEVERITIES:
        raise PolicyError(f"{where}: severity must be one of {SEVERITIES}, got '{severity}'")

    groups_raw = raw.get("groups", ["all"])
    if isinstance(groups_raw, str):
        groups_raw = [groups_raw]
    if not isinstance(groups_raw, list) or not groups_raw:
        raise PolicyError(f"{where}: 'groups' must be a non-empty list")
    groups = frozenset(str(g).strip().lower() for g in groups_raw)

    present = _compile_patterns(raw.get("match_present"), where, "match_present")
    absent = _compile_patterns(raw.get("match_absent"), where, "match_absent")
    if not present and not absent:
        raise PolicyError(f"{where}: needs 'match_present' and/or 'match_absent'")

    unknown = set(raw) - {"id", "description", "severity", "groups", "match_present", "match_absent"}
    if unknown:
        raise PolicyError(f"{where}: unknown keys {sorted(unknown)}")

    return Rule(
        id=rule_id,
        description=description,
        severity=severity,
        groups=groups,
        match_present=present,
        match_absent=absent,
        source=str(file),
    )


def _compile_patterns(value, where: str, key: str) -> tuple[re.Pattern, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list):
        raise PolicyError(f"{where}: '{key}' must be a string or a list of strings")
    patterns = []
    for pat in value:
        try:
            patterns.append(re.compile(str(pat), re.MULTILINE))
        except re.error as exc:
            raise PolicyError(f"{where}: invalid regex in '{key}': {pat!r} ({exc})") from exc
    return tuple(patterns)
