from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

#: A fabric device config that satisfies every rule in the shipped packs.
COMPLIANT_FABRIC_CONFIG = """\
config terminal
boot config flags sshd
boot config flags spbm-config-mode
sys name "core-01"
web-server secure-only
cli timeout 900
password min-passwd-len 12
banner custom
banner "authorized access only"
snmp-server community s3cret-ro
spbm
spbm 1
spbm 1 nick-name 0.10.01
router isis
   sys-name "core-01"
   manual-area 49.0001
exit
router isis enable
ntp server 10.0.0.100
end
"""

#: An edge device violating several security rules.
VIOLATING_EDGE_CONFIG = """\
config terminal
boot config flags telnetd
boot config flags ftpd
snmp-server community public
cli timeout 900
password min-passwd-len 8
banner custom
web-server secure-only
boot config flags sshd
end
"""


@pytest.fixture
def compliant_config() -> str:
    return COMPLIANT_FABRIC_CONFIG


@pytest.fixture
def violating_config() -> str:
    return VIOLATING_EDGE_CONFIG


@pytest.fixture
def policies_dir() -> Path:
    return REPO_ROOT / "policies"


@pytest.fixture
def inventory_csv(tmp_path: Path) -> Path:
    path = tmp_path / "inventory.csv"
    path.write_text(
        "hostname,ip,groups\n"
        "core-01,10.0.0.1,fabric;core\n"
        "edge-01,10.0.10.1,\n"
    )
    return path
