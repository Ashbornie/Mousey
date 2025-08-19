## Mousey - Hand-Tracking Mouse Control (Windows) 🖱️🖐️

### Overview ✨
Control your mouse cursor using hand gestures captured from your webcam. This project uses OpenCV for video capture, MediaPipe for real-time hand landmark detection, and `pynput` to move the system cursor and perform clicks/scrolls.

### Tech Stack 🧰
- **Language**: [Python](https://www.python.org/) 3.8–3.12 🐍
- **Computer Vision**: [OpenCV](https://opencv.org/) 📷
- **Hand Tracking**: [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) ✋
- **Input Control**: [`pynput`](https://pypi.org/project/pynput/) ⌨️
- **Math/Utils**: [NumPy](https://numpy.org/) 🔢
- **OS**: Windows 10/11 🪟

### Features ✅
- **Natural cursor control**: Move your right hand to move the cursor.
- **Scroll gesture**: Pinch your right index finger and thumb to enable scroll, then move up/down to scroll.
- **Click-and-drag**: Pinch your left index finger and thumb to press/hold the left mouse button; release to drop.
- **Dynamic DPI awareness**: Automatically adapts to your primary display resolution.

### Requirements 🧩
- Windows 10/11 (x64)
- A working webcam
- Python 3.8–3.12 (recommended)

MediaPipe provides prebuilt wheels for Windows x64 for Python 3.8–3.12. If you are on Python 3.13, please create a Python 3.12 virtual environment (instructions below). Using the same interpreter for both `python` and `pip` is essential.

### Folder structure 📁
```
Ashborn/
└─ Mousey/
   ├─ README.md               ← you are here
   ├─ main.py                 ← the app entry point (create/restore if missing)
   └─ env/                    ← optional virtual environment (do not commit; add to .gitignore)
```

### Quick start 🚀
1) Open a terminal.

2) Create and activate a virtual environment (PowerShell):
```powershell
py -3.12 -m venv env
./env/Scripts/Activate.ps1
```
If `py -3.12` is not available, use whatever Python in the 3.8–3.12 range you have installed, e.g. `py -3.10 -m venv env` or `python -m venv env`.

3) Upgrade tooling and install dependencies:
```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install mediapipe==0.10.14 opencv-python numpy pynput
```

4) Run the app:
```powershell
python main.py
```

### Gestures and controls 🎮
- **Move cursor (Right hand)**: Move your right hand; the cursor follows your right index fingertip.
- **Scroll (Right hand pinch)**: Pinch right thumb and index to start scrolling; move hand vertically to scroll. Release to stop.
- **Click & drag (Left hand pinch)**: Pinch left thumb and index to press/hold left button; move to drag; release to drop.

### Configuration ⚙️
Adjust these parameters in `main.py` to suit your setup:
- **`pinch_threshold`**: Distance (normalized) at which a pinch is detected. Increase if clicks/scrolls trigger too easily; decrease if they do not trigger.
- **`scroll_sensitivity`**: Scales how fast the page scrolls during a pinch.
- **Camera index**: If the webcam does not open, change `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` (or another index).
- **Multi-monitor setups**: Current mapping targets the primary monitor. If you have multiple displays, you may need custom mapping logic.

### Troubleshooting MediaPipe installation 🛠️
If you see `ModuleNotFoundError: No module named 'mediapipe'` or `ERROR: Could not build wheels for mediapipe`:

1) Verify Python and pip match the same interpreter:
```powershell
python -V
python -m pip -V
```
Ensure the `pip` path points to your active virtual environment.

2) Ensure you are on a supported Python version (3.8–3.12 on Windows x64). If you’re on 3.13, create a 3.12 environment:
```powershell
py -3.12 -m venv env
./env/Scripts/Activate.ps1
```

3) Upgrade build tools and retry installation:
```powershell
python -m pip install --upgrade pip setuptools wheel
python -m pip install mediapipe==0.10.14
```

4) If corporate/firewall restrictions block downloads, configure your proxy for pip or try another network.

5) As a last resort, download a wheel that matches your Python and platform from [MediaPipe on PyPI](https://pypi.org/project/mediapipe/) and install it:
```powershell
python -m pip install path\to\mediapipe‑0.10.14‑cp312‑cp312‑win_amd64.whl
```
Replace the filename to match your Python minor version (e.g., `cp310` for Python 3.10).

### Other common issues ❓
- **Webcam not opening**: Use a different camera index; ensure the camera is not in use by another app; allow Camera access under Windows Privacy settings.
- **Cursor movement is jumpy**: Add smoothing or increase the movement threshold in the code before updating `mouse.position`.
- **App cannot control the mouse**: Some security software blocks simulated input; try running your terminal as Administrator or allow `pynput` behavior.

### Development notes 📝
- This project uses MediaPipe Hands for landmark detection and OpenCV for frames.
- On high-DPI displays, the script queries the primary screen resolution to map normalized landmarks to pixel coordinates.
- If `main.py` is currently missing, recreate it with the logic described above or restore it from version control.

### References 🔗
- [MediaPipe documentation](https://developers.google.com/mediapipe)
- [MediaPipe on PyPI](https://pypi.org/project/mediapipe/)
- [OpenCV](https://opencv.org/)
- [`pynput` on PyPI](https://pypi.org/project/pynput/)

### License 📄
If a `LICENSE` file is present in the repository, that license applies. Otherwise, consider adding an open-source license (e.g., MIT) to clarify usage rights.


