# 📸 Peace-Sign Selfie App  
### ✌️ AI-Powered Gesture Selfie with Filters  

This lightweight Python app uses **OpenCV** and **MediaPipe** to detect a ✌️ *(peace sign)* gesture and automatically take a **selfie** with a fun filter after a short countdown.  

Built with passion by [@tubakhxn](https://github.com/tubakhxn) 💻✨  

---

## 🚀 Features  
- ✌️ Detects **peace sign** gesture (index + middle fingers up).  
- ⏱️ 2-second countdown overlay before capturing the photo.  
- 🎨 Applies a simple **AI-style filter** (grayscale, sepia, or cartoon).  
- 💾 Saves both original and filtered selfies as:  
  - `selfie_YYYYMMDD_HHMMSS.jpg`  
  - `filtered_selfie_YYYYMMDD_HHMMSS.jpg`  
- 🔊 Plays a short beep sound on Windows after capture.  
- 📷 Displays live webcam feed with hand tracking landmarks.  

---

## 📁 Files Created  
- `selfie_colab.ipynb` — Colab notebook (browser-camera compatible)  
- `selfie_app.py` — Standalone local Python app  
- `requirements.txt` — Minimal dependency list  

---

## ⚙️ Quick Install (Windows / PowerShell)  
```powershell
# Create a virtual environment (recommended)
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## ▶️ Run (Local Machine)  
```powershell
python selfie_app.py
```

---

## 🧠 How It Works  
1. Opens your webcam and mirrors the live preview.  
2. Uses **MediaPipe** to track your hand landmarks.  
3. Detects the ✌️ **peace sign** (index & middle up, others down).  
4. Starts a **2-second countdown overlay** on the feed.  
5. Captures the selfie, saves both versions, plays a beep (on Windows), and shows the filtered selfie.  

---

## ⚡ Performance Tips  
- Sets **model complexity = 0** for lighter CPU load.  
- Tracks **only one hand** for efficiency.  
- Optionally skip frames by adjusting `FRAME_SKIP` in `selfie_app.py`.  
- Default resolution: **640×480**.  

---

## 🧩 Customization  
- Change the `FILTER` variable to:  
  - `grayscale`, `sepia`, `cartoon`, or `None`  
- Adjust `DELAY_SECONDS` for countdown duration.  
- Tune `MODEL_COMPLEXITY` for performance vs. accuracy.  

---

## ☁️ Colab Notes  
The included notebook `selfie_colab.ipynb` works with your browser’s camera inside Google Colab.  
> ⚠️ Colab uses JS webcam APIs — expect higher latency compared to local runs.  

---

## 💡 Extra Options  
You can:  
- Add a GUI overlay (button or status bar).  
- Enable simple logging / debugging.  
- Run syntax & lint checks to optimize frame timing.  

---

## 👤 Author & Credits  
**Project by:** [@tubakhxn](https://github.com/tubakhxn)  

💬 Feel free to **fork** and remix the project — but please **don’t just copy and re-upload** as your own.  
If you liked it, ⭐ the repo and comment “peace” to get project links on my socials ✌️  

---

## 📄 License  
**MIT License** — open to use, share, and modify with credit to **tubakhxn**.  
