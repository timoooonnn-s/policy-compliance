"""Reporting: JUnit XML for GitLab and a console summary for pipeline logs."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path

from .engine import DeviceAudit


def write_junit(audits: list[DeviceAudit], path: str | Path) -> None:
    """One <testsuite> per device, one <testcase> per evaluated rule.

    A device whose config could not be collected gets a single errored
    testcase, so unreachable devices are visible in GitLab's Tests tab.
    """
    suites = ET.Element("testsuites", name="voss-audit")
    for audit in audits:
        suite = ET.SubElement(suites, "testsuite", name=audit.device.hostname)
        if audit.error is not None:
            case = ET.SubElement(
                suite, "testcase", classname=audit.device.hostname, name="collect-running-config"
            )
            ET.SubElement(case, "error", message=audit.error)
            _set_counts(suite, tests=1, failures=0, errors=1)
            continue

        failures = 0
        for result in audit.results:
            rule = result.rule
            case = ET.SubElement(
                suite,
                "testcase",
                classname=audit.device.hostname,
                name=f"{rule.id}: {rule.description} [{rule.severity}]",
            )
            if not result.passed:
                failures += 1
                ET.SubElement(case, "failure", message=result.message)
        _set_counts(suite, tests=len(audit.results), failures=failures, errors=0)

    tree = ET.ElementTree(suites)
    ET.indent(tree)
    tree.write(path, encoding="unicode", xml_declaration=True)


def _set_counts(suite: ET.Element, tests: int, failures: int, errors: int) -> None:
    suite.set("tests", str(tests))
    suite.set("failures", str(failures))
    suite.set("errors", str(errors))


def print_summary(audits: list[DeviceAudit]) -> None:
    width = max([len(a.device.hostname) for a in audits] + [len("Device")])
    print(f"\n{'Device':<{width}}  {'Rules':>5}  {'Passed':>6}  {'Failed':>6}  Status")
    print("-" * (width + 32))
    for audit in audits:
        host = audit.device.hostname
        if audit.error is not None:
            print(f"{host:<{width}}  {'-':>5}  {'-':>6}  {'-':>6}  ERROR: {audit.error}")
        else:
            failed = len(audit.failed)
            status = "FAIL" if failed else "OK"
            print(
                f"{host:<{width}}  {len(audit.results):>5}  "
                f"{len(audit.results) - failed:>6}  {failed:>6}  {status}"
            )

    violations = [(a, r) for a in audits for r in a.failed]
    if violations:
        print(f"\nViolations ({len(violations)}):")
        for audit, result in violations:
            rule = result.rule
            print(f"  [{rule.severity.upper():>8}] {audit.device.hostname}  "
                  f"{rule.id}: {rule.description}")
            print(f"             {result.message}")
    errors = [a for a in audits if a.error is not None]
    if errors:
        print(f"\nUnreachable/errored devices ({len(errors)}): "
              + ", ".join(a.device.hostname for a in errors))
    print()
