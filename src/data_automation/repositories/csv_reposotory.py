import csv
from pathlib import Path
from data_automation.models import ParsedEvent


def load_events_from_csv(path: Path) -> tuple[list[ParsedEvent], list[str]]:
    results = []
    errors = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        if not validate_headers(headers):
            raise ValueError(
                f"File has incorrect headers. Expected: ['id', 'machine', 'duration_s'], Got: {headers}"
            )
        for i, row in enumerate(reader, start=2):
            try:
                row["duration_s"] = int(row["duration_s"])
                results.append(row)
            except (ValueError, KeyError, TypeError) as e:
                error_msg = f"Error {e} in row {i}"
                errors.append(error_msg)

    return results, errors


def validate_headers(headers) -> bool:
    expected_headers = ["id", "machine", "duration_s"]
    return headers == expected_headers
