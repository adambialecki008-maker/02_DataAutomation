from xlsx_repository import export_downtime_to_excel
from openpyxl import load_workbook, workbook
from pathlib import Path
from main import generate_report
from datetime import date
import pytest

BASE_DIR = Path(__file__).resolve().parent
source_path = BASE_DIR / "fixtures" / "downtime_200_test.csv"


@pytest.fixture
def report_sheet(tmp_path):
    output_path = tmp_path / "test_report_path"
    output_path.mkdir()
    report = generate_report(source_path)
    export_downtime_to_excel(report, output_path)
    today = date.today()
    title = f"Downtime Report_{today}"
    file_path = output_path / f"{title}.xlsx"
    wb = load_workbook(file_path)
    ws = wb.active
    return ws


def test_export_downtime_to_excel_returns_workbook(report_sheet):

    ws = report_sheet
    assert ws is not None
    assert ws["A1"].value == "Machine name"


def test_export_downtime_to_excel_returns_correct_data_for_first_machine(report_sheet):
    ws = report_sheet
    assert ws["A2"].value == "PRESS_1"
    assert ws["B2"].value == 17
    assert ws["C2"].value == 17310


def test_export_downtime_to_excel_returns_correct_data_for_total(report_sheet):
    ws = report_sheet
    last_row = ws.max_row
    assert ws[f"A{last_row}"].value == "Total"
    assert ws[f"B{last_row}"].value == 138
    assert ws[f"C{last_row}"].value == 161430


def test_export_downtime_to_excel_returns_correct_data_for_rejected(report_sheet):
    ws = report_sheet
    assert ws["E2"].value == 62


def test_export_downtime_to_excel_returns_correct_data_for_empty_sheet(tmp_path):
    report = {
        "machines": {},
        "rejected": 0,
    }
    output_path = tmp_path / "test_report_path"
    output_path.mkdir()
    export_downtime_to_excel(report, output_path)
    today = date.today()
    title = f"Downtime Report_{today}"
    file_path = output_path / f"{title}.xlsx"
    wb = load_workbook(file_path)
    ws = wb.active
    assert ws is not None
    last_row = ws.max_row
    assert ws[f"A{last_row}"].value == "Total"
    assert ws[f"B{last_row}"].value == 0
    assert ws[f"C{last_row}"].value == 0
    assert ws.max_row == 2
    assert ws["A2"].value == "Total"
