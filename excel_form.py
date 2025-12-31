from __future__ import annotations

from io import BytesIO
from typing import Iterable, List

from openpyxl import load_workbook


def extract_headers(stream: BytesIO) -> List[str]:
    """Read the first row of the first sheet and return non-empty headers.

    Raises:
        ValueError: If no headers are found.
    """

    workbook = load_workbook(stream, data_only=True)
    sheet = workbook.active

    headers: List[str] = []
    for cell in sheet[1]:  # first row
        if cell.value is None or str(cell.value).strip() == "":
            continue
        headers.append(str(cell.value).strip())

    if not headers:
        raise ValueError("No headers were found in the first row of the workbook.")

    return headers


def fill_template(template_bytes: bytes, row_data: Iterable[str]) -> bytes:
    """Fill the first worksheet of a template workbook with one row of data.

    The input workbook is not modified; a new workbook is returned as bytes.
    """

    workbook = load_workbook(BytesIO(template_bytes))
    sheet = workbook.active

    # Write data starting at the second row to preserve headers
    for column_index, value in enumerate(row_data, start=1):
        sheet.cell(row=2, column=column_index, value=value)

    output = BytesIO()
    workbook.save(output)
    return output.getvalue()
