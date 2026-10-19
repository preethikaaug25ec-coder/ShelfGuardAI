
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_from_directory
)
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime
import json
import os

from shelf_analyzer import analyze_image

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "inspections.json"

UPLOAD_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "change-this-development-key"
)
app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def load_inspections():
    if not DATA_FILE.exists():
        return []

    try:
        return json.loads(
            DATA_FILE.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        return []


def save_inspections(records):
    DATA_FILE.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8"
    )


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


@app.route("/")
def dashboard():
    inspections = load_inspections()

    alerts = []
    for record in reversed(inspections):
        for alert in record.get("alerts", []):
            alerts.append({
                **alert,
                "aisle": record["aisle"],
                "created_at": record["created_at"]
            })

    total_detections = sum(
        record.get("product_count", 0)
        for record in inspections
    )

    misplaced_count = sum(
        alert["type"] == "Misplaced item"
        for record in inspections
        for alert in record.get("alerts", [])
    )

    stockout_count = sum(
        alert["type"] == "Possible stockout"
        for record in inspections
        for alert in record.get("alerts", [])
    )

    return render_template(
        "dashboard.html",
        inspections=inspections,
        alerts=alerts[:8],
        total_detections=total_detections,
        misplaced_count=misplaced_count,
        stockout_count=stockout_count
    )


@app.route("/inspect", methods=["GET", "POST"])
def inspect():
    if request.method == "GET":
        return render_template("inspect.html")

    image = request.files.get("shelf_image")
    aisle = request.form.get("aisle", "Aisle 7").strip()
    shelf = request.form.get("shelf", "Shelf 3").strip()
    mode = request.form.get("mode", "demo")

    if not image or not image.filename:
        flash("Please choose a shelf image.", "error")
        return redirect(url_for("inspect"))

    if not allowed_file(image.filename):
        flash("Upload PNG, JPG, JPEG, or WEBP images.", "error")
        return redirect(url_for("inspect"))

    filename = secure_filename(image.filename)
    unique_name = (
        datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        + "_" + filename
    )

    image_path = UPLOAD_DIR / unique_name
    image.save(image_path)

    result = analyze_image(image_path, mode)

    record = {
        "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
        "created_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "aisle": aisle[:60],
        "shelf": shelf[:60],
        "image": unique_name,
        "mode": result["mode"],
        "product_count": result["product_count"],
        "detections": result["detections"],
        "alerts": result["alerts"],
        "note": result["note"]
    }

    records = load_inspections()
    records.append(record)
    save_inspections(records)

    return render_template("result.html", item=record)


@app.route("/history")
def history():
    records = list(reversed(load_inspections()))
    return render_template(
        "history.html", inspections=records
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.route("/clear-history", methods=["POST"])
def clear_history():
    save_inspections([])
    flash("Inspection history cleared.", "success")
    return redirect(url_for("history"))


@app.errorhandler(413)
def file_too_large(error):
    flash("Image size must be 12 MB or less.", "error")
    return redirect(url_for("inspect"))


if __name__ == "__main__":
    app.run(debug=True)
