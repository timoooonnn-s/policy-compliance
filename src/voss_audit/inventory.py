"""Load the device inventory from a CSV file.

Expected format (header required, groups column optional):

    hostname,ip,groups
    core-01,10.0.0.1,fabric;core
    edge-01,10.0.10.1,

Groups may be separated by ";" or whitespace (or "," inside a quoted field).
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


class InventoryError(Exception):
    """Raised when the inventory CSV is missing or malformed."""


@dataclass(frozen=True)
class Device:
    hostname: str
    ip: str
    groups: frozenset[str]


_GROUP_SPLIT = re.compile(r"[;,\s]+")


def load_inventory(path: str | Path) -> list[Device]:
    path = Path(path)
    if not path.is_file():
        raise InventoryError(f"inventory file not found: {path}")

    with path.open(newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        fields = [f.strip().lower() for f in reader.fieldnames or []]
        if "hostname" not in fields or "ip" not in fields:
            raise InventoryError(
                f"{path}: header must contain 'hostname' and 'ip' columns, got: {fields}"
            )
        # Normalize header names so "Hostname" / "IP " also work.
        reader.fieldnames = fields

        devices: list[Device] = []
        seen: set[str] = set()
        for lineno, row in enumerate(reader, start=2):
            hostname = (row.get("hostname") or "").strip()
            ip = (row.get("ip") or "").strip()
            if not hostname and not ip:
                continue  # blank line
            if not hostname or not ip:
                raise InventoryError(f"{path}:{lineno}: hostname and ip must both be set")
            if hostname in seen:
                raise InventoryError(f"{path}:{lineno}: duplicate hostname '{hostname}'")
            seen.add(hostname)

            raw_groups = (row.get("groups") or "").strip()
            groups = frozenset(g.lower() for g in _GROUP_SPLIT.split(raw_groups) if g)
            devices.append(Device(hostname=hostname, ip=ip, groups=groups))

    if not devices:
        raise InventoryError(f"{path}: no devices found")
    return devices
