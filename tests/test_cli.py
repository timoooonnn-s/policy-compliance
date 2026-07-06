import pytest

from voss_audit import cli
from voss_audit.collector import CollectionResult
from voss_audit.engine import DeviceAudit, RuleResult
from voss_audit.inventory import Device
from voss_audit.rules import Rule
from tests.conftest import COMPLIANT_FABRIC_CONFIG, VIOLATING_EDGE_CONFIG


def _fake_collector(configs_by_host):
    def collect(devices, username, password, **kwargs):
        results = []
        for d in devices:
            value = configs_by_host.get(d.hostname)
            if value is None:
                results.append(CollectionResult(device=d, error="TimeoutError: unreachable"))
            else:
                results.append(CollectionResult(device=d, config=value))
        return results

    return collect


@pytest.fixture
def env(monkeypatch):
    monkeypatch.setenv("VOSS_USERNAME", "auditor")
    monkeypatch.setenv("VOSS_PASSWORD", "secret")


def _run(monkeypatch, inventory_csv, tmp_path, configs, extra_args=()):
    monkeypatch.setattr(cli, "collect_configs", _fake_collector(configs))
    junit = tmp_path / "report.xml"
    rc = cli.main([
        "--inventory", str(inventory_csv),
        "--policies", "policies",
        "--junit", str(junit),
        *extra_args,
    ])
    return rc, junit


def test_all_compliant_exits_zero(monkeypatch, env, inventory_csv, tmp_path):
    rc, junit = _run(monkeypatch, inventory_csv, tmp_path, {
        "core-01": COMPLIANT_FABRIC_CONFIG,
        "edge-01": COMPLIANT_FABRIC_CONFIG,
    })
    assert rc == 0
    assert junit.is_file()


def test_violations_fail_at_threshold(monkeypatch, env, inventory_csv, tmp_path):
    configs = {"core-01": COMPLIANT_FABRIC_CONFIG, "edge-01": VIOLATING_EDGE_CONFIG}
    rc, _ = _run(monkeypatch, inventory_csv, tmp_path, configs)
    assert rc == 1  # default --fail-on high; edge has critical violations
    rc, _ = _run(monkeypatch, inventory_csv, tmp_path, configs, ["--fail-on", "never"])
    assert rc == 0


def test_unreachable_device_fails_run(monkeypatch, env, inventory_csv, tmp_path):
    rc, _ = _run(monkeypatch, inventory_csv, tmp_path, {
        "core-01": COMPLIANT_FABRIC_CONFIG,  # edge-01 missing -> collection error
    }, ["--fail-on", "never"])
    assert rc == 1


def test_host_filter(monkeypatch, env, inventory_csv, tmp_path):
    rc, _ = _run(monkeypatch, inventory_csv, tmp_path,
                 {"core-01": COMPLIANT_FABRIC_CONFIG},
                 ["--host", "core-01"])
    assert rc == 0
    rc = cli.main(["--inventory", str(inventory_csv), "--policies", "policies",
                   "--host", "nope-01"])
    assert rc == 2


def test_missing_credentials(monkeypatch, inventory_csv):
    monkeypatch.delenv("VOSS_USERNAME", raising=False)
    monkeypatch.delenv("VOSS_PASSWORD", raising=False)
    rc = cli.main(["--inventory", str(inventory_csv), "--policies", "policies"])
    assert rc == 2


def test_lint_mode_needs_no_credentials(monkeypatch, inventory_csv, capsys):
    monkeypatch.delenv("VOSS_USERNAME", raising=False)
    rc = cli.main(["--inventory", str(inventory_csv), "--policies", "policies", "--lint"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "2 device(s)" in out


def test_lint_catches_bad_policy(tmp_path, inventory_csv):
    bad = tmp_path / "bad.yml"
    bad.write_text("rules:\n  - id: X\n")
    rc = cli.main(["--inventory", str(inventory_csv), "--policies", str(bad), "--lint"])
    assert rc == 2


def _mkrule(severity):
    import re
    return Rule(id=f"T-{severity}", description="t", severity=severity,
                groups=frozenset({"all"}), match_present=(re.compile("x"),),
                match_absent=(), source="test")


def test_exit_code_thresholds():
    device = Device(hostname="d", ip="1.1.1.1", groups=frozenset())
    audit = DeviceAudit(device=device, results=[
        RuleResult(rule=_mkrule("medium"), passed=False, message="m"),
    ])
    assert cli.exit_code([audit], "high") == 0
    assert cli.exit_code([audit], "medium") == 1
    assert cli.exit_code([audit], "never") == 0
    errored = DeviceAudit(device=device, error="boom")
    assert cli.exit_code([errored], "never") == 1
