import pytest

from voss_audit.inventory import InventoryError, load_inventory


def test_load_inventory(inventory_csv):
    devices = load_inventory(inventory_csv)
    assert [d.hostname for d in devices] == ["core-01", "edge-01"]
    assert devices[0].ip == "10.0.0.1"
    assert devices[0].groups == {"fabric", "core"}
    assert devices[1].groups == frozenset()


def test_missing_file(tmp_path):
    with pytest.raises(InventoryError, match="not found"):
        load_inventory(tmp_path / "nope.csv")


def test_missing_columns(tmp_path):
    path = tmp_path / "bad.csv"
    path.write_text("name,address\nsw1,10.0.0.1\n")
    with pytest.raises(InventoryError, match="header"):
        load_inventory(path)


def test_duplicate_hostname(tmp_path):
    path = tmp_path / "dup.csv"
    path.write_text("hostname,ip\nsw1,10.0.0.1\nsw1,10.0.0.2\n")
    with pytest.raises(InventoryError, match="duplicate"):
        load_inventory(path)


def test_empty_inventory(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("hostname,ip,groups\n")
    with pytest.raises(InventoryError, match="no devices"):
        load_inventory(path)


def test_groups_without_column(tmp_path):
    path = tmp_path / "min.csv"
    path.write_text("hostname,ip\nsw1,10.0.0.1\n")
    (device,) = load_inventory(path)
    assert device.groups == frozenset()


def test_quoted_comma_groups(tmp_path):
    path = tmp_path / "quoted.csv"
    path.write_text('hostname,ip,groups\nsw1,10.0.0.1,"fabric, core"\n')
    (device,) = load_inventory(path)
    assert device.groups == {"fabric", "core"}
