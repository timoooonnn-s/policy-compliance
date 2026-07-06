import pytest

from voss_audit.rules import PolicyError, load_policies


def test_shipped_policy_packs_are_valid(policies_dir):
    rules = load_policies(policies_dir)
    ids = [r.id for r in rules]
    assert len(ids) == len(set(ids))
    assert any(r.id.startswith("SEC-") for r in rules)
    assert any(r.id.startswith("FAB-") for r in rules)
    fabric_rules = [r for r in rules if r.id.startswith("FAB-")]
    assert all(r.groups == {"fabric"} for r in fabric_rules)


def test_single_file(tmp_path):
    file = tmp_path / "p.yml"
    file.write_text(
        "rules:\n"
        "  - id: X-1\n"
        "    description: test\n"
        "    severity: low\n"
        "    match_present: ['^a', '^b']\n"
    )
    (rule,) = load_policies(file)
    assert rule.groups == {"all"}
    assert len(rule.match_present) == 2


@pytest.mark.parametrize(
    ("body", "error"),
    [
        ("rules:\n  - description: d\n    severity: low\n    match_present: a\n", "'id' is required"),
        ("rules:\n  - id: X\n    severity: low\n    match_present: a\n", "'description' is required"),
        ("rules:\n  - id: X\n    description: d\n    severity: urgent\n    match_present: a\n", "severity"),
        ("rules:\n  - id: X\n    description: d\n    severity: low\n", "match_present"),
        ("rules:\n  - id: X\n    description: d\n    severity: low\n    match_present: '('\n", "invalid regex"),
        ("rules:\n  - id: X\n    description: d\n    severity: low\n    match_present: a\n    bogus: 1\n", "unknown keys"),
        ("notrules: []\n", "top-level 'rules' list"),
    ],
)
def test_invalid_rules(tmp_path, body, error):
    file = tmp_path / "bad.yml"
    file.write_text(body)
    with pytest.raises(PolicyError, match=error):
        load_policies(file)


def test_duplicate_ids_across_files(tmp_path):
    rule = "rules:\n  - id: X-1\n    description: d\n    severity: low\n    match_present: a\n"
    (tmp_path / "a.yml").write_text(rule)
    (tmp_path / "b.yml").write_text(rule)
    with pytest.raises(PolicyError, match="duplicate rule id"):
        load_policies(tmp_path)


def test_empty_dir(tmp_path):
    with pytest.raises(PolicyError, match="no .yml"):
        load_policies(tmp_path)
