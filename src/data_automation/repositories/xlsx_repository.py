from openpyxl import Workbook
from pathlib import Path
from datetime import date
from openpyxl.styles import Font, PatternFill
from copy import copy
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter


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
    style_headers(ws)
    set_columns_width(ws)
    file_path = output_path / f"{title}.xlsx"
    wb.save(file_path)


def style_headers(ws: Worksheet) -> None:
    headers_font = Font(bold=True, size=12, color="FFFFFF", italic=True)
    headers_fill = PatternFill(fill_type="solid", fgColor="1F4E78")
    total_font = copy(headers_font)
    total_font.color = "1F2937"
    total_font.italic = False
    total_fill = copy(headers_fill)
    total_fill.fgColor = "D9EAF7"
    headers, total_row = get_headers_and_total_row(ws)
    for header in headers:
        header.font = headers_font
        header.fill = headers_fill
    for cell in total_row:
        cell.font = total_font
        cell.fill = total_fill


def set_columns_width(ws: Worksheet) -> None:
    columns = ws.iter_cols()
    for index, column in enumerate(columns, start=1):
        max_length = 0
        for cell in column:
            if cell.value is not None:
                lenght = len(str(cell.value))
                if lenght > max_length:
                    max_length = lenght
        column_letter = get_column_letter(index)
        ws.column_dimensions[column_letter].width = max_length + 3


def get_headers_and_total_row(ws: Worksheet) -> tuple[list, list]:
    headers = [
        ws["A1"],
        ws["B1"],
        ws["C1"],
        ws["E1"],
    ]
    last_row = ws.max_row
    total_row = [
        ws[f"A{last_row}"],
        ws[f"B{last_row}"],
        ws[f"C{last_row}"],
    ]
    return headers, total_row
