import os
import sys
import uuid
import hashlib
import traceback
from flask import Flask, render_template, request, jsonify, url_for, send_from_directory, abort
from threading import Timer
from werkzeug.utils import secure_filename

# Optional: GPU control
USE_CUDA = os.getenv("USE_CUDA", "1").lower() in ("1", "true", "yes")

# -------------------------------------------------------------------------
# Resource handling for both development and PyInstaller bundle
# -------------------------------------------------------------------------
def resource_path(rel: str) -> str:
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base = os.path.abspath(".")
    return os.path.join(base, rel)

# -------------------------------------------------------------------------
# Directory setup (write-safe)
# -------------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    base_appdata = os.path.join(os.getenv("APPDATA"), "Splasher")
    UPLOAD_FOLDER = os.path.join(base_appdata, "uploads")
    RESULT_FOLDER = os.path.join(base_appdata, "results")
else:
    UPLOAD_FOLDER = os.path.join("static", "uploads")
    RESULT_FOLDER = os.path.join("static", "results")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

MODEL_PATH = resource_path("best.pt")

# -------------------------------------------------------------------------
# Imports
# -------------------------------------------------------------------------
try:
    from ultralytics import YOLO
    import torch
    import cv2
except Exception as e:
    print("Error importing modules:", e)
    sys.exit(1)

# -------------------------------------------------------------------------
# Model loading
# -------------------------------------------------------------------------
try:
    print(f"Loading model from {MODEL_PATH}")
    model = YOLO(MODEL_PATH)
    device = "cuda:0" if USE_CUDA and torch.cuda.is_available() else "cpu"
    print(f"✅ Model loaded successfully on device: {device}")
except Exception as e:
    print("❌ Model load failed:", e)
    traceback.print_exc()
    sys.exit(1)

# -------------------------------------------------------------------------
# Flask setup
# -------------------------------------------------------------------------
app = Flask(
    __name__,
    static_folder=resource_path("static"),
    template_folder=resource_path("templates")
)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

# -------------------------------------------------------------------------
# Utility functions
# -------------------------------------------------------------------------
def name_to_hex(name: str) -> str:
    h = hashlib.md5(name.encode()).hexdigest()
    r = int(h[0:2], 16)
    g = int(h[2:4], 16)
    b = int(h[4:6], 16)
    def bump(x): return int(80 + (x / 255.0) * 175)
    return '#{:02x}{:02x}{:02x}'.format(bump(r), bump(g), bump(b))

# -------------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------------
@app.route("/")
def index():
    # Read optional 'sat' query parameter so template can highlight selection
    selected = request.args.get("sat", "")
    return render_template("index.html", selected_sat=selected)

# ensure satellite endpoint exists (prevents BuildError in templates)
@app.route("/satellite/<sat>")
def satellite(sat):
    # Render the same template but indicate which satellite is selected
    return render_template("index.html", selected_sat=sat)

# serve favicon if present in static folder (prevents 404)
@app.route("/favicon.ico")
def favicon():
    fav_path = os.path.join(app.static_folder, "favicon.ico")
    if os.path.isfile(fav_path):
        return send_from_directory(app.static_folder, "favicon.ico")
    # if favicon not found, return 404 so browser won't keep requesting it
    abort(404)

@app.route("/api/process", methods=["POST"])
def process():
    try:
        if "images[]" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        file = request.files["images[]"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        results = model.predict(source=filepath, imgsz=1280, conf=0.25, device=device, save=False)
        result = results[0]

        names_map = model.names or {}
        class_counts = {name: 0 for name in names_map.values()}

        confs = result.boxes.conf.cpu().numpy()
        cls_ids = result.boxes.cls.cpu().numpy().astype(int)
        xyxy = result.boxes.xyxy.cpu().numpy()

        for conf, cid in zip(confs, cls_ids):
            if conf >= 0.25:
                cname = names_map.get(cid, str(cid))
                class_counts[cname] = class_counts.get(cname, 0) + 1

        total = sum(class_counts.values())
        class_colors = {name: name_to_hex(name) for name in names_map.values()}

        # Draw results
        img = cv2.imread(filepath)
        h, w = img.shape[:2]
        thickness = max(3, int(round(min(h, w) / 200.0)))

        for conf, cid, box in zip(confs, cls_ids, xyxy):
            if conf < 0.25:
                continue
            cname = names_map.get(cid, str(cid))
            hexcol = class_colors.get(cname, "#cccccc")
            r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
            color = (b, g, r)
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

        result_filename = f"result_{filename}"
        result_path = os.path.join(app.config["RESULT_FOLDER"], result_filename)
        cv2.imwrite(result_path, img)

        processed_url = url_for("static", filename=f"results/{result_filename}")
        return jsonify({
            "processedImages": [{"url": processed_url, "downloadUrl": processed_url}],
            "detections": class_counts,
            "classColors": class_colors,
            "total": total
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route("/static/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/static/results/<filename>")
def serve_result(filename):
    return send_from_directory(app.config["RESULT_FOLDER"], filename)

# -------------------------------------------------------------------------
# Auto open browser
# -------------------------------------------------------------------------
def open_browser():
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000/")

if __name__ == "__main__":
    if getattr(sys, 'frozen', False):
        Timer(1, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)
