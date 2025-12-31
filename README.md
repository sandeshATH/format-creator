# format-creator

A simple Flask app that turns the first row of any uploaded Excel (.xlsx) workbook into a web form. Upload your template, enter data into the generated form, and download a new Excel file with your responses written to the first data row.

## Quick start

1. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   flask --app app run
   ```

4. Open the app at http://127.0.0.1:5000. Upload an `.xlsx` file that contains your column headers in the first row, fill out the generated form, and download the filled workbook.

## How it works

- The first row of the first worksheet is treated as column headers. Empty header cells are ignored.
- After uploading, the template is kept in the session so you can submit the form immediately.
- Submitted values are written to the second row of the template, preserving your header row and any formatting in the rest of the sheet.
- Downloads use the original filename prefixed with `filled_`.

## Testing

Run unit tests with:

```bash
pytest
```

## Configuration

Set `SECRET_KEY` to override the default development secret if you deploy the app:
```bash
export SECRET_KEY="a-long-random-string"
```
