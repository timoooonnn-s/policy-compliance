import xml.etree.ElementTree as ET

from voss_audit.engine import DeviceAudit, evaluate
from voss_audit.inventory import Device
from voss_audit.report import print_summary, write_junit
from voss_audit.rules import load_policies

FABRIC = Device(hostname="core-01", ip="10.0.0.1", groups=frozenset({"fabric"}))
EDGE = Device(hostname="edge-01", ip="10.0.10.1", groups=frozenset())
DOWN = Device(hostname="down-01", ip="10.0.99.1", groups=frozenset())


def _audits(policies_dir, compliant_config, violating_config):
    rules = load_policies(policies_dir)
    return [
        DeviceAudit(device=FABRIC, results=evaluate(FABRIC, compliant_config, rules)),
        DeviceAudit(device=EDGE, results=evaluate(EDGE, violating_config, rules)),
        DeviceAudit(device=DOWN, error="TimeoutError: connect timed out"),
    ]


def test_junit_report(tmp_path, policies_dir, compliant_config, violating_config):
    audits = _audits(policies_dir, compliant_config, violating_config)
    out = tmp_path / "report.xml"
    write_junit(audits, out)

    root = ET.parse(out).getroot()
    assert root.tag == "testsuites"
    suites = {s.get("name"): s for s in root}
    assert set(suites) == {"core-01", "edge-01", "down-01"}

    core = suites["core-01"]
    assert core.get("failures") == "0"
    assert int(core.get("tests")) == len(audits[0].results)

    edge = suites["edge-01"]
    assert int(edge.get("failures")) == len(audits[1].failed)
    failure_cases = [c for c in edge if c.find("failure") is not None]
    assert len(failure_cases) == len(audits[1].failed)
    assert all("[" in c.get("name") for c in edge)  # severity in the test name

    down = suites["down-01"]
    assert down.get("errors") == "1"
    (case,) = list(down)
    assert case.find("error").get("message").startswith("TimeoutError")


def test_print_summary(capsys, policies_dir, compliant_config, violating_config):
    print_summary(_audits(policies_dir, compliant_config, violating_config))
    out = capsys.readouterr().out
    assert "core-01" in out and "OK" in out
    assert "FAIL" in out
    assert "SEC-001" in out
    assert "down-01" in out and "ERROR" in out
