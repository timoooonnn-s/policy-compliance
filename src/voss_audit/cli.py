"""Command line entry point for voss-audit."""

from __future__ import annotations

import argparse
import logging
import os
import sys

from . import SEVERITIES, __version__
from .collector import DEFAULT_COMMAND, collect_configs
from .engine import DeviceAudit, applicable_rules, evaluate
from .inventory import InventoryError, load_inventory
from .report import print_summary, write_junit
from .rules import PolicyError, load_policies


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="voss-audit",
        description="Audit Extreme VOSS/VSP switches against YAML policy rules.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--inventory", default="inventory.csv",
                        help="device CSV (hostname,ip,groups) [default: %(default)s]")
    parser.add_argument("--policies", default="policies",
                        help="directory with policy .yml files, or a single file "
                             "[default: %(default)s]")
    parser.add_argument("--junit", metavar="FILE",
                        help="write a JUnit XML report to FILE")
    parser.add_argument("--workers", type=int, default=10,
                        help="parallel SSH connections [default: %(default)s]")
    parser.add_argument("--timeout", type=int, default=30,
                        help="SSH connect timeout in seconds [default: %(default)s]")
    parser.add_argument("--fail-on", choices=[*SEVERITIES, "never"], default="high",
                        help="lowest violation severity that makes the run exit non-zero; "
                             "'never' ignores violations [default: %(default)s]")
    parser.add_argument("--host", action="append", metavar="HOSTNAME",
                        help="audit only this device (repeatable)")
    parser.add_argument("--group", action="append", metavar="GROUP",
                        help="audit only devices in this group (repeatable)")
    parser.add_argument("--show-command", default=DEFAULT_COMMAND,
                        help="command used to fetch the config [default: %(default)s]")
    parser.add_argument("--lint", action="store_true",
                        help="only validate inventory and policy files, no device access")
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose logging")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format="%(levelname)s %(name)s: %(message)s",
    )

    try:
        devices = load_inventory(args.inventory)
        rules = load_policies(args.policies)
    except (InventoryError, PolicyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.host:
        wanted = set(args.host)
        unknown = wanted - {d.hostname for d in devices}
        if unknown:
            print(f"error: host(s) not in inventory: {', '.join(sorted(unknown))}",
                  file=sys.stderr)
            return 2
        devices = [d for d in devices if d.hostname in wanted]
    if args.group:
        wanted_groups = {g.lower() for g in args.group}
        devices = [d for d in devices if d.groups & wanted_groups]
        if not devices:
            print(f"error: no devices in group(s): {', '.join(sorted(wanted_groups))}",
                  file=sys.stderr)
            return 2

    if args.lint:
        print(f"OK: {len(devices)} device(s), {len(rules)} rule(s)")
        for device in devices:
            n = len(applicable_rules(rules, device))
            groups = ",".join(sorted(device.groups)) or "-"
            print(f"  {device.hostname} ({device.ip})  groups: {groups}  rules: {n}")
        return 0

    username = os.environ.get("VOSS_USERNAME")
    password = os.environ.get("VOSS_PASSWORD")
    if not username or not password:
        print("error: VOSS_USERNAME and VOSS_PASSWORD environment variables must be set",
              file=sys.stderr)
        return 2

    collections = collect_configs(
        devices, username, password,
        workers=args.workers, timeout=args.timeout, command=args.show_command,
    )

    audits: list[DeviceAudit] = []
    for coll in collections:
        if coll.error is not None:
            audits.append(DeviceAudit(device=coll.device, error=coll.error))
        else:
            audits.append(DeviceAudit(
                device=coll.device,
                results=evaluate(coll.device, coll.config or "", rules),
            ))

    print_summary(audits)
    if args.junit:
        write_junit(audits, args.junit)
        print(f"JUnit report written to {args.junit}")

    return exit_code(audits, args.fail_on)


def exit_code(audits: list[DeviceAudit], fail_on: str) -> int:
    """Collection errors always fail; violations fail at/above the threshold."""
    if any(a.error is not None for a in audits):
        return 1
    if fail_on == "never":
        return 0
    threshold = SEVERITIES.index(fail_on)
    for audit in audits:
        for result in audit.failed:
            if SEVERITIES.index(result.rule.severity) >= threshold:
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
