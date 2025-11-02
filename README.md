Peace-sign Selfie App
======================

This small Python app uses OpenCV and Mediapipe to detect a ✌️ (peace sign) hand gesture and automatically take a selfie after a short countdown. A simple filter is applied to the saved selfie and the filtered image is shown.

Files created
- `selfie_colab.ipynb`  — Colab-compatible notebook (already created).
- `selfie_app.py`       — Standalone Python script for local use (this file).
- `requirements.txt`    — Minimal Python dependencies.

Quick install (Windows / PowerShell)

```powershell
# create a virtual environment (recommended)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run (local machine)

```powershell
python selfie_app.py
```

How it works
- Opens your webcam and shows a mirrored live preview.
- Uses Mediapipe to track a single hand and draws landmarks.
- If the peace sign is detected (index+middle up, ring+pinky down, fingers separated), it starts a 2-second countdown overlay.
- After the countdown it saves `selfie_YYYYMMDD_HHMMSS.jpg` and `filtered_selfie_...jpg` to the same folder, plays a short beep (Windows), and displays the filtered result.

Performance / "faster" tips used
- Model complexity is set to 0 (lower cost) and only 1 hand is tracked to reduce CPU.
- Optionally skip frames with `FRAME_SKIP` in `selfie_app.py` to process fewer frames per second.
- Frame size defaults to 640x480.

Customization
- Change `FILTER` in `selfie_app.py` to `grayscale`, `sepia`, `cartoon`, or `None`.
- Adjust `DELAY_SECONDS` for a longer/shorter countdown.
- Increase/decrease `MODEL_COMPLEXITY` for more/less accuracy.

Notes
- The Colab notebook uses browser camera APIs and is suitable for running inside Google Colab.
- The standalone script is intended for local use (Windows, macOS, Linux). On Windows the script attempts a simple beep using `winsound`.

If you want, I can now:
- Run a quick syntax/lint check here, or
- Add a GUI-based small status overlay/button, or
- Add logging and a small test harness.

Which would you like next?