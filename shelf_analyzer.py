
from pathlib import Path


def analyze_image(image_path: Path, mode="demo"):
    """
    Demo mode provides simulated results.
    AI mode attempts general-object detection using YOLO.
    """

    if mode == "demo":
        return {
            "mode": "Demo simulation",
            "product_count": 18,
            "detections": [
                {
                    "name": "Product A (demo)",
                    "count": 7,
                    "confidence": 0.94,
                    "position": "Left section"
                },
                {
                    "name": "Product B (demo)",
                    "count": 6,
                    "confidence": 0.89,
                    "position": "Center section"
                },
                {
                    "name": "Product C (demo)",
                    "count": 5,
                    "confidence": 0.86,
                    "position": "Right section"
                }
            ],
            "alerts": [
                {
                    "type": "Misplaced item",
                    "severity": "High",
                    "message": (
                        "Demo alert: Product B is outside "
                        "its expected shelf zone."
                    )
                },
                {
                    "type": "Possible stockout",
                    "severity": "Medium",
                    "message": (
                        "Demo alert: Product C is below "
                        "the configured shelf minimum."
                    )
                }
            ],
            "note": (
                "Simulated results only. These values "
                "were not calculated from the uploaded image."
            )
        }

    if mode == "auto":
        try:
            from ultralytics import YOLO

            model = YOLO("yolov8n.pt")
            prediction = model(str(image_path), verbose=False)[0]

            detections = []

            for box in prediction.boxes:
                class_id = int(box.cls[0].item())
                confidence = float(box.conf[0].item())
                name = prediction.names[class_id]

                coordinates = [
                    round(float(value), 1)
                    for value in box.xyxy[0].tolist()
                ]

                detections.append({
                    "name": name,
                    "count": 1,
                    "confidence": round(confidence, 3),
                    "position": str(coordinates)
                })

            alerts = [{
                "type": "Review required",
                "severity": "Low",
                "message": (
                    "General objects were detected. "
                    "A store-specific SKU model and "
                    "planogram are needed to verify placement."
                )
            }]

            if not detections:
                alerts = [{
                    "type": "No objects detected",
                    "severity": "Medium",
                    "message": (
                        "No supported objects were found. "
                        "Check image quality and model coverage."
                    )
                }]

            return {
                "mode": "YOLO general-object detection",
                "product_count": len(detections),
                "detections": detections[:100],
                "alerts": alerts,
                "note": (
                    "YOLO detects general object categories. "
                    "Results are not guaranteed retail SKU counts "
                    "and cannot prove stockouts or planogram violations."
                )
            }

        except ImportError:
            return {
                "mode": "AI unavailable",
                "product_count": 0,
                "detections": [],
                "alerts": [{
                    "type": "AI model unavailable",
                    "severity": "Medium",
                    "message": (
                        "Install the optional ultralytics package "
                        "to enable AI mode."
                    )
                }],
                "note": (
                    "Choose Demo mode to demonstrate the interface "
                    "without installing the AI model."
                )
            }

        except Exception as error:
            return {
                "mode": "Analysis error",
                "product_count": 0,
                "detections": [],
                "alerts": [{
                    "type": "Analysis error",
                    "severity": "Medium",
                    "message": (
                        f"Image analysis failed: "
                        f"{type(error).__name__}"
                    )
                }],
                "note": (
                    "No reliable shelf conclusion could be reached."
                )
            }

    return {
        "mode": "Invalid mode",
        "product_count": 0,
        "detections": [],
        "alerts": [],
        "note": "Choose Demo or AI mode."
    }
