from voss_audit.engine import applicable_rules, evaluate
from voss_audit.inventory import Device
from voss_audit.rules import load_policies

FABRIC = Device(hostname="core-01", ip="10.0.0.1", groups=frozenset({"fabric", "core"}))
EDGE = Device(hostname="edge-01", ip="10.0.10.1", groups=frozenset())


def test_group_targeting(policies_dir):
    rules = load_policies(policies_dir)
    fabric_ids = {r.id for r in applicable_rules(rules, FABRIC)}
    edge_ids = {r.id for r in applicable_rules(rules, EDGE)}
    assert any(i.startswith("FAB-") for i in fabric_ids)
    assert not any(i.startswith("FAB-") for i in edge_ids)
    assert all(i.startswith("SEC-") for i in edge_ids)


def test_compliant_fabric_device(policies_dir, compliant_config):
    rules = load_policies(policies_dir)
    results = evaluate(FABRIC, compliant_config, rules)
    failed = [r for r in results if not r.passed]
    assert failed == [], [f"{r.rule.id}: {r.message}" for r in failed]


def test_violating_edge_device(policies_dir, violating_config):
    rules = load_policies(policies_dir)
    results = evaluate(EDGE, violating_config, rules)
    failed = {r.rule.id for r in results if not r.passed}
    assert "SEC-001" in failed  # telnetd enabled
    assert "SEC-003" in failed  # ftpd enabled
    assert "SEC-006" in failed  # snmp community public
    assert "SEC-002" not in failed  # sshd is enabled


def test_failure_messages_include_pattern_and_line(policies_dir, violating_config):
    rules = load_policies(policies_dir)
    results = {r.rule.id: r for r in evaluate(EDGE, violating_config, rules)}
    telnet = results["SEC-001"]
    assert "boot config flags telnetd" in telnet.message  # the offending line
    absent_banner = results["SEC-005"]
    assert absent_banner.passed


def test_no_prefix_confusion():
    """'no boot config flags telnetd' must NOT trip the ^-anchored absent rule."""
    rules = load_policies("policies")
    config = "no boot config flags telnetd\nboot config flags sshd\n"
    results = {r.rule.id: r for r in evaluate(EDGE, config, rules)}
    assert results["SEC-001"].passed
