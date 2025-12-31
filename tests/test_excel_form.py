from io import BytesIO

import pytest
from openpyxl import Workbook, load_workbook

from excel_form import extract_headers, fill_template


def build_workbook(headers):
    wb = Workbook()
    ws = wb.active
    for col, header in enumerate(headers, start=1):
        ws.cell(row=1, column=col, value=header)
    buffer = BytesIO()
    wb.save(buffer)
    return buffer.getvalue()


def test_extract_headers_returns_values_from_first_row():
    headers = ["Name", "Email", "Age"]
    workbook_bytes = build_workbook(headers)

    result = extract_headers(BytesIO(workbook_bytes))

    assert result == headers


def test_extract_headers_raises_when_no_headers():
    workbook_bytes = build_workbook([""])

    with pytest.raises(ValueError):
        extract_headers(BytesIO(workbook_bytes))


def test_fill_template_writes_data_in_second_row():
    headers = ["Name", "Email"]
    workbook_bytes = build_workbook(headers)

    filled_bytes = fill_template(workbook_bytes, ["Ada", "ada@example.com"])

    workbook = load_workbook(BytesIO(filled_bytes))
    sheet = workbook.active

    assert sheet.cell(row=2, column=1).value == "Ada"
    assert sheet.cell(row=2, column=2).value == "ada@example.com"
