# format-creator

A simple Flask app that turns the first row of any uploaded Excel (.xlsx) workbook into a web form. Upload your template, enter data into the generated form, and download a new Excel file with your responses written to the first data row.

## Quick start

1) Create and activate a virtual environment (recommended):
```bash
python -m venv .venv
source .venv/bin/activate
```

2) Install dependencies:
```bash
pip install -r requirements.txt
```

3) Export an app secret (optional but recommended for production):
```bash
export SECRET_KEY="a-long-random-string"
```

4) Start the Flask server (either approach works):
```bash
# Using the flask CLI
flask --app app run

# Or directly with Python
python app.py
```

5) In your browser, open http://127.0.0.1:5000 and follow the flow:
   - Upload an `.xlsx` file whose **first row contains your column headers**.
   - Fill in the generated web form for those headers.
   - Download the resulting Excel file; your entries are written to the first data row while preserving the template formatting.

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

If dependencies are missing in your environment, install them first:
```bash
pip install -r requirements.txt
```

## Configuration

Set `SECRET_KEY` to override the default development secret if you deploy the app:
```bash
export SECRET_KEY="a-long-random-string"
```
