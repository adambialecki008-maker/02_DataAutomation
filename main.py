from pathlib import Path
from csv_reposotory import load_events_from_csv
from downtime_analyzer import analyze_downtime

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "tests" / "fixtures" / "downtime_200_test.csv"

events = load_events_from_csv(csv_path)
analyzed = analyze_downtime(events)
print(analyzed)
