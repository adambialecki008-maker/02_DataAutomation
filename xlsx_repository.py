from openpyxl import Workbook
from pathlib import Path
from datetime import date


def export_downtime_to_excel(report: dict, output_path: Path) -> None:
    wb = Workbook()
    ws = wb.active
    today = date.today()
    assert ws is not None
    title = f"Downtime Report_{today}"
    ws.title = title
    ws.append(["Machine name", "count", "total_stop_s"])
    ws.cell(row=1, column=5, value="Rejected")
    rejected = report["rejected"]
    machines = report["machines"]
    total_counts = 0
    total_stops = 0
    ##Append data from reports to
    for name, data in machines.items():
        count = data["count"]
        total_counts += count
        total_stop_s = data["total_stop_s"]
        total_stops += total_stop_s
        ws.append([name, count, total_stop_s])

    ws.append(["Total", total_counts, total_stops])
    ws.cell(row=2, column=5, value=rejected)

    file_path = output_path / f"{title}.xlsx"
    wb.save(file_path)
