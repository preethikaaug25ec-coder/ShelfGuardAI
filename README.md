
# ShelfGuard AI

### AI-Powered Retail Shelf Intelligence Platform

**Tagline:** We don't just detect products. We understand whether the shelf is correct.

## Problem Statement

Manual shelf audits are slow. Stockouts can cause lost sales, misplaced
products reduce visibility, and delayed restocking affects customer
experience. Planogram violations can remain unnoticed between audits.

## Proposed Solution

ShelfGuard AI is a software-only prototype designed to analyze retail
shelf images and help store teams review shelf conditions.

## Features

- Shelf image upload
- Aisle and shelf identification
- Object detection using optional YOLO integration
- Simulated demo detections and alerts
- Potential stock issue alerts
- Planogram-related review alerts
- Dashboard with summary metrics and chart
- Inspection history
- Responsive web interface

## Technology Stack

- Python
- Flask
- HTML
- CSS
- JavaScript
- Chart.js
- Optional Ultralytics YOLO

## System Workflow

1. Upload an image from an existing camera or phone.
2. Select the aisle and shelf.
3. Run demo mode or optional general-object detection.
4. Review detected objects and alerts.
5. Save and review the inspection history.

## Important Limitations

Demo results are simulated. The pretrained general-object detector
does not reliably identify retail SKUs, verify a store planogram,
or establish that a product is out of stock.

A production system requires a retail-product dataset, a trained
product detection model, store-specific planogram data, and testing.

## Run Locally

Install Python 3.10 or newer.

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## Project Structure

```text
ShelfGuardAI/
├── app.py
├── shelf_analyzer.py
├── requirements.txt
├── README.md
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── inspect.html
│   ├── result.html
│   └── history.html
├── static/
│   └── style.css
├── uploads/
└── data/
```

## Future Improvements

- Retail SKU recognition
- Planogram editor
- Shelf-level product counting
- Persistent camera-feed processing
- Confidence-based alerts
- Restocking recommendations
- Human confirmation workflow

## Project Type

Academic and hackathon prototype.

## License

Add a license before publishing if required.
