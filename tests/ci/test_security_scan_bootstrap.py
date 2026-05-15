# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import importlib.util
from pathlib import Path

SCRIPT_PATH = Path(__file__).parents[2] / "scripts" / "security_scan.py"
AGENT_OS_SRC = (
    Path(__file__).parents[2] / "agent-governance-python" / "agent-os" / "src"
)


def load_security_scan_module():
    spec = importlib.util.spec_from_file_location("security_scan", SCRIPT_PATH)
    assert spec is not None
    security_scan = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(security_scan)
    return security_scan


def test_security_scan_loads_agent_os_from_flattened_layout() -> None:
    security_scan = load_security_scan_module()

    assert AGENT_OS_SRC in security_scan.AGENT_OS_SOURCE_ROOTS
    assert Path(security_scan._security_skills.__file__) == (
        AGENT_OS_SRC / "agent_os" / "security_skills.py"
    )


def test_security_scan_import_exposes_scan_source() -> None:
    security_scan = load_security_scan_module()

    findings = security_scan.scan_source(
        "def verify():\n"
        "    return True\n",
        "example.py",
    )

    assert findings
    assert findings[0].rule_id == "SKILL-001"
