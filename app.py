import os
from io import BytesIO
from pathlib import Path
from typing import List
from uuid import uuid4

from flask import Flask, flash, redirect, render_template, request, send_file, session, url_for
from werkzeug.utils import secure_filename

from excel_form import extract_fields, fill_template


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")
UPLOAD_DIR = Path(app.instance_path) / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.route("/")
def index():
    has_template = "template_id" in session
    return render_template("index.html", has_template=has_template)


@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files.get("template")
    if not uploaded_file or uploaded_file.filename == "":
        flash("Please choose an Excel file before uploading.")
        return redirect(url_for("index"))

    filename = secure_filename(uploaded_file.filename)
    if not filename.lower().endswith(".xlsx"):
        flash("Only .xlsx files are supported.")
        return redirect(url_for("index"))

    file_bytes = uploaded_file.read()
    if not file_bytes:
        flash("The uploaded file is empty.")
        return redirect(url_for("index"))

    try:
        fields = extract_fields(BytesIO(file_bytes))
    except ValueError as exc:  # raised when no headers are found
        flash(str(exc))
        return redirect(url_for("index"))
    except Exception:
        flash("Unable to read that workbook. Make sure it is a valid .xlsx file.")
        return redirect(url_for("index"))

    template_id = f"{uuid4().hex}.xlsx"
    template_path = UPLOAD_DIR / template_id
    template_path.write_bytes(file_bytes)
    session["template_id"] = template_id
    session["fields"] = fields
    session["template_name"] = filename
    flash("Template uploaded. Fill out the generated form below.")
    return redirect(url_for("fill"))


@app.route("/fill", methods=["GET", "POST"])
def fill():
    template_id = session.get("template_id")
    fields: List[dict] = session.get("fields", [])

    if not template_id or not fields:
        flash("Upload a template first.")
        return redirect(url_for("index"))

    template_path = UPLOAD_DIR / template_id
    if not template_path.exists():
        flash("Template file is missing. Please upload again.")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("fill.html", fields=fields)

    # POST: create a filled workbook
    row_data = [request.form.get(field["key"], "") for field in fields]
    template_name = session.get("template_name", "template.xlsx")

    workbook_bytes = fill_template(template_path.read_bytes(), fields, row_data)
    download_name = f"filled_{template_name}" if not template_name.startswith("filled_") else template_name

    return send_file(
        BytesIO(workbook_bytes),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=download_name,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
