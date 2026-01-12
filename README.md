# 🛰️ Cantonment Area Detection System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Object%20Detection-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

An advanced AI-powered application designed to detect and analyze features within Cantonment areas using satellite imagery. This project leverages **YOLOv8** for state-of-the-art object detection and **Flask** for a responsive web interface.

## ✨ Features

- **Object Detection**: Automatically identifies key structures (Buildings, Roads, Vegetation, etc.) from satellite images.
- **Interactive UI**: Clean, web-based interface for uploading images and viewing results.
- **Dual Mode**:
  - **Web Application**: Run locally via browser.
  - **Standalone Executable**: No-install `.exe` version available.
- **Reporting**: Generates breakdown of detected classes and counts.

## 🛠️ Tech Stack

- **Backend**: Python, Flask, OpenCV
- **AI/ML**: Ultralytics YOLOv8 (PyTorch)
- **Frontend**: HTML5, CSS3, JavaScript
- **Packaging**: PyInstaller

## 🚀 Getting Started

### Option A: Download Executable (Easiest)
Go to the [Releases Page](../../releases) and download `Cantonment Area Detection.exe`.
Double-click to run! No installation required.

### Option B: Run from Source

1.  **Clone the repository**
    ```bash
    git clone https://github.com/samirkumar13/Cantonment-Area-Detection.git
    cd Cantonment-Area-Detection
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Add Model File**
    > **Note**: The trained model `best.pt` is not included in this public repo for security reasons.
    > You must place your `best.pt` file in the root directory.

5.  **Run the App**
    ```bash
    python app.py
    ```
    Open your browser to `http://127.0.0.1:5000`.


## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---
*Built by [Samir Kumar](https://github.com/samirkumar13)*
