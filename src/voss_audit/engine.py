"""Evaluate policy rules against a device's running-config text."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .inventory import Device
from .rules import Rule


@dataclass(frozen=True)
class RuleResult:
    rule: Rule
    passed: bool
    message: str = ""


@dataclass
class DeviceAudit:
    """Everything the reports need to know about one device."""

    device: Device
    error: str | None = None  # set if the config could not be collected
    results: list[RuleResult] = field(default_factory=list)

    @property
    def failed(self) -> list[RuleResult]:
        return [r for r in self.results if not r.passed]


def applicable_rules(rules: list[Rule], device: Device) -> list[Rule]:
    return [r for r in rules if "all" in r.groups or r.groups & device.groups]


def evaluate(device: Device, config: str, rules: list[Rule]) -> list[RuleResult]:
    return [_check(rule, config) for rule in applicable_rules(rules, device)]


def _check(rule: Rule, config: str) -> RuleResult:
    problems = []
    for pattern in rule.match_present:
        if not pattern.search(config):
            problems.append(f"required pattern not found: {pattern.pattern!r}")
    for pattern in rule.match_absent:
        match = pattern.search(config)
        if match:
            line = _line_of(config, match)
            problems.append(f"forbidden pattern {pattern.pattern!r} matched: {line!r}")
    if problems:
        return RuleResult(rule=rule, passed=False, message="; ".join(problems))
    return RuleResult(rule=rule, passed=True)


def _line_of(config: str, match: re.Match) -> str:
    start = config.rfind("\n", 0, match.start()) + 1
    end = config.find("\n", match.end())
    if end == -1:
        end = len(config)
    return config[start:end].strip()
