# 🖥 PC Activity Logger → Google Sheets

This script logs **process activity** and **active window titles** from your computer directly into a **Google Sheet** in real-time.  
It works on **Windows** and **Linux** (with minor setup differences).

---

## 📦 Features
- Logs every new process with:
  - Timestamp
  - Process name
  - Active window title
- Saves data to **Google Sheets** using the Google Drive API
- Can be **remotely stopped** by typing `STOP` in cell `D1` of the Google Sheet
- Cross-platform (Windows & Linux)

---

## ⚙️ Setup

### 1️⃣ Get Google Sheets API Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or use an existing one).
3. Enable **Google Sheets API** and **Google Drive API**.
4. Go to **Credentials** → Create **Service Account** → Create **JSON Key**.
5. Download the `.json` file and rename it to `credentials.json`.
6. Share your target Google Sheet with the service account's email (found inside the JSON file).

---

### 2️⃣ Install Dependencies

#### **Windows**
```bash
pip install psutil gspread oauth2client pywin32
sudo apt install xdotool wmctrl
pip install psutil gspread oauth2client
3️⃣ Prepare Your Google Sheet

    Create a new Google Sheet and name it PC Activity Logger (or update the name in the script).

    Leave it blank — the script will automatically add headers.

    The script will create:

    Time | Process Name | Window Title

    Cell D1 will contain the status — change it to STOP to stop the script remotely.

🚀 Usage
Windows

Use the Windows version of the script:

import psutil
import win32gui
...

Run it:

python activity_logger_windows.py

Linux

Use the Linux version of the script:

import psutil
import subprocess
...

Run it:

python activity_logger_linux.py

🛑 Stopping the Script

    You can stop it remotely by changing cell D1 in the Google Sheet to:

STOP

Or locally with:

    Ctrl + C

⚠️ Notes

    On Linux, xdotool must be installed or active window titles will not be detected.

    On Windows, pywin32 must be installed for window title detection.

    The Google Sheets API has a rate limit — avoid excessively short update intervals.

📜 License

This project is free to use and modify for personal purposes.


---

If you want, I can also **merge** the Windows & Linux code into one **single cross-platform script** so that this README only needs one usage section.  
That way you don’t have to maintain two separate files.

