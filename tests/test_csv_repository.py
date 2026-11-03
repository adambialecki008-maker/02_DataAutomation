from csv_reposotory import validate_headers, load_events_from_csv
from pathlib import Path
import pytest

BASE_DIR = Path(__file__).resolve().parent


def test_validate_headers_rejects_wrong_headers():
    headers = ["idi", "machine_name", "duration_s"]
    assert validate_headers(headers) == False


def test_validate_headers_accepts_expected_headers():
    headers = ["id", "machine", "duration_s"]
    assert validate_headers(headers) == True


def test_load_files_from_csv_loads_dict_list():
    csv_path = BASE_DIR / "fixtures" / "downtime_200_test.csv"
    events = load_events_from_csv(csv_path)
    assert len(events) == 200
    durations = set()
    for event in events:
        durations.add(event["duration_s"])
    assert "abc" in durations


def test_load_files_from_csv_returns_0_on_empty_file():
    csv_path = BASE_DIR / "fixtures" / "downtime_empty.csv"
    events = load_events_from_csv(csv_path)
    assert len(events) == 0


def test_load_files_from_csv_raises_if_no_file():
    csv_path = BASE_DIR / "fixtures" / "downtime_empty2.csv"

    with pytest.raises(FileNotFoundError):
        load_events_from_csv(csv_path)
