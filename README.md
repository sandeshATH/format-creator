# format-creator

A simple Flask app that turns bold fields in an uploaded Excel (.xlsx) workbook into a web form. Upload your template, enter data into the generated form, and download a new Excel file with your responses written back into the same cells.

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

4. Open the app at http://127.0.0.1:5000. Upload an `.xlsx` file, fill out the generated form for bold fields, and download the filled workbook.

## How it works

- The app looks for bold cells in column E where column A contains the label.
- After uploading, the template is stored on disk and referenced by the session so you can submit the form immediately.
- Submitted values are written back into the same bold cells, preserving formatting and formulas elsewhere.
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
