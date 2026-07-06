"""Fetch running configs from VOSS/VSP switches over SSH, in parallel.

One device failing (unreachable, auth error, timeout) never affects the
others - the error is captured per device and reported downstream.
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass

from .inventory import Device

log = logging.getLogger(__name__)

DEFAULT_COMMAND = "show running-config"


@dataclass
class CollectionResult:
    device: Device
    config: str | None = None
    error: str | None = None


def collect_configs(
    devices: list[Device],
    username: str,
    password: str,
    workers: int = 10,
    timeout: int = 30,
    command: str = DEFAULT_COMMAND,
) -> list[CollectionResult]:
    """Fetch the config of every device concurrently. Order matches `devices`."""

    def fetch(device: Device) -> CollectionResult:
        log.info("collecting config from %s (%s)", device.hostname, device.ip)
        try:
            config = _fetch_config(device, username, password, timeout, command)
            return CollectionResult(device=device, config=config)
        except Exception as exc:  # any per-device failure must not stop the run
            log.warning("failed to collect %s: %s", device.hostname, exc)
            return CollectionResult(device=device, error=f"{type(exc).__name__}: {exc}")

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        return list(pool.map(fetch, devices))


def _fetch_config(
    device: Device, username: str, password: str, timeout: int, command: str
) -> str:
    # Imported lazily so the rest of the toolkit (lint, tests) works without netmiko.
    from netmiko import ConnectHandler

    conn = ConnectHandler(
        device_type="extreme_vsp",
        host=device.ip,
        username=username,
        password=password,
        conn_timeout=timeout,
    )
    try:
        return conn.send_command(command, read_timeout=max(timeout, 90))
    finally:
        conn.disconnect()
