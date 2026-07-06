# voss-audit — policy compliance for Extreme VOSS/VSP switches

A small Python toolkit that SSHes into your Extreme VOSS/VSP switches, pulls the
running configuration, checks it against versioned YAML policy rules, and emits
a JUnit XML report that GitLab CI renders natively. **Report-only** — it never
changes device state.

- 2 dependencies: [netmiko](https://github.com/ktbyers/netmiko) (SSH) and PyYAML. Everything else is stdlib.
- Devices are audited **in parallel** and **independently** — an unreachable
  switch is reported as an error but never stops the others.
- Rules have **severity levels**; the pipeline fails only at/above a
  configurable threshold.

## Quick start

```bash
uv pip install --system .          # or: pip install .

export VOSS_USERNAME=auditor
export VOSS_PASSWORD=...

voss-audit --inventory inventory.csv --policies policies/ --junit report.xml
```

Validate inventory and rules without touching any device:

```bash
voss-audit --lint
```

## Inventory (CSV)

`inventory.csv` — one row per switch, `groups` column optional:

```csv
hostname,ip,groups
core-01,10.0.0.1,fabric;core
edge-01,10.0.10.1,
```

Groups are separated by `;` (or quoted `,`). Rules can target groups; devices
without groups get only the rules targeting `all`.

## Policy rules (YAML)

All `*.yml` files in `policies/` are loaded. A rule needs an `id`,
`description`, `severity` (`info|low|medium|high|critical`) and at least one of:

- `match_present` — regex(es) that **must** match the running config
- `match_absent` — regex(es) that **must not** match

Patterns run with `re.MULTILINE` against the raw config text, so `^` anchors to
line starts. Optional `groups:` restricts a rule to inventory groups
(default: `all`).

```yaml
rules:
  - id: SEC-001
    description: Telnet must be disabled
    severity: critical
    match_absent: '^boot config flags telnetd'
  - id: FAB-003
    description: SPBM nick-name must be assigned
    severity: high
    groups: [fabric]
    match_present: '^spbm \d+ nick-name'
```

Two starter packs ship in `policies/`: `security-hardening.yml` (all devices)
and `fabric-consistency.yml` (group `fabric`).

> **Adapt the patterns.** `show running-config` output differs between VOSS
> firmware versions and only lists non-default settings. Verify each rule
> against your devices' actual output before enforcing it (a quick check:
> run with `--host <one-device>` and read the report).

## CLI reference

| Option | Default | Purpose |
|---|---|---|
| `--inventory` | `inventory.csv` | device CSV |
| `--policies` | `policies` | rule directory or single file |
| `--junit FILE` | – | write JUnit XML report |
| `--workers N` | `10` | parallel SSH connections |
| `--timeout N` | `30` | SSH connect timeout (seconds) |
| `--fail-on SEV` | `high` | lowest severity that fails the run; `never` disables |
| `--host H` | – | audit only this device (repeatable) |
| `--group G` | – | audit only this group (repeatable) |
| `--show-command CMD` | `show running-config` | config fetch command |
| `--lint` | – | validate files only, no device access |

**Exit codes:** `0` compliant (below threshold) · `1` violations at/above
threshold **or** unreachable devices · `2` usage/config errors.

Credentials come from the `VOSS_USERNAME` / `VOSS_PASSWORD` environment
variables.

## GitLab CI

`.gitlab-ci.yml` ships two jobs:

- **lint-policies** — validates inventory + rules on merge requests and pushes
  to the default branch. No device access, safe to run anywhere.
- **compliance-audit** — the real audit. Runs on **scheduled pipelines**
  (CI/CD → Schedules, e.g. nightly) and manual web-triggered pipelines. Uploads
  `report.xml` as a JUnit artifact so results appear in the pipeline **Tests**
  tab.

Setup:

1. Set `VOSS_USERNAME` / `VOSS_PASSWORD` as **masked** CI/CD variables
   (Settings → CI/CD → Variables).
2. Create a pipeline schedule (e.g. nightly).
3. Make sure the runner can reach the switches' management IPs over SSH —
   tag the job/runner if only specific runners have that access.

## Development

```bash
uv sync            # installs the package + dev deps into .venv
uv run pytest      # toolkit's own tests (no network needed)
uv run ruff check
```
