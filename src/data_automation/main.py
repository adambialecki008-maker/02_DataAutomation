from pathlib import Path
from data_automation.repositories.csv_reposotory import load_events_from_csv
from data_automation.downtime_analyzer import analyze_downtime


def generate_report(source_path: Path) -> dict:
    events, import_errors = load_events_from_csv(source_path)
    analyze = analyze_downtime(events)
    rejected = analyze["rejected"] + len(import_errors)
    errors = {"import": import_errors, "validation": analyze["errors"]}
    report = {"machines": analyze["machines"], "rejected": rejected, "errors": errors}
    return report


if __name__ == "__main__":
    file_path = Path("tests/fixtures/downtime_200_test.csv")
    print(generate_report(file_path))
