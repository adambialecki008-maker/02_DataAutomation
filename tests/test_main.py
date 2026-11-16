from data_automation.main import generate_report
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "fixtures" / "downtime_mixed_validation.csv"


def test_generate_report_succes():
    report = generate_report(file_path)
    machines = report["machines"]
    rejected = report["rejected"]
    errors_import = report["errors"]["importing"]
    errors_validation = report["errors"]["validation"]
    accepted = sum(machine["count"] for machine in machines.values())
    assert rejected == 11
    assert len(machines) == 5
    assert accepted == 7
    assert len(errors_import) == 5
    assert len(errors_validation) == 6
