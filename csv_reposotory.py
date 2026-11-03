import csv
from pathlib import Path


def load_events_from_csv(path: Path) -> list[dict]:
    results = []
    errors = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames
        if not validate_headers(headers):
            raise ValueError(
                f"File has incorrect headers. Expected: ['id', 'machine', 'duration_s'], Got: {headers}"
            )
        for row in reader:
            try:
                row["duration_s"] = int(row["duration_s"])
            except (ValueError, KeyError, TypeError) as e:
                errors.append(e)
            results.append(row)

    return results


def validate_headers(headers) -> bool:
    expected_headers = ["id", "machine", "duration_s"]
    return headers == expected_headers
