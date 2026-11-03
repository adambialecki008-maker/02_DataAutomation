from pathlib import Path
from csv_reposotory import load_events_from_csv
from downtime_analyzer import analyze_downtime


def generate_report(source_path: Path) -> dict:
    events = load_events_from_csv(source_path)
    report = analyze_downtime(events)
    return report
