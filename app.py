import base64
import os
from io import BytesIO
from typing import List

from flask import Flask, flash, redirect, render_template, request, send_file, session, url_for
from werkzeug.utils import secure_filename

from excel_form import extract_headers, fill_template


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")


@app.route("/")
def index():
    has_template = "template" in session
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
        headers = extract_headers(BytesIO(file_bytes))
    except ValueError as exc:  # raised when no headers are found
        flash(str(exc))
        return redirect(url_for("index"))
    except Exception:
        flash("Unable to read that workbook. Make sure it is a valid .xlsx file.")
        return redirect(url_for("index"))

    session["template"] = base64.b64encode(file_bytes).decode("utf-8")
    session["headers"] = headers
    session["template_name"] = filename
    flash("Template uploaded. Fill out the generated form below.")
    return redirect(url_for("fill"))


@app.route("/fill", methods=["GET", "POST"])
def fill():
    template_b64 = session.get("template")
    headers: List[str] = session.get("headers", [])

    if not template_b64 or not headers:
        flash("Upload a template first.")
        return redirect(url_for("index"))

    if request.method == "GET":
        return render_template("fill.html", headers=headers)

    # POST: create a filled workbook
    row_data = [request.form.get(header, "") for header in headers]
    template_name = session.get("template_name", "template.xlsx")

    workbook_bytes = fill_template(base64.b64decode(template_b64), row_data)
    download_name = f"filled_{template_name}" if not template_name.startswith("filled_") else template_name

    return send_file(
        BytesIO(workbook_bytes),
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        as_attachment=True,
        download_name=download_name,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
