import psutil
import subprocess
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ========== SETUP GOOGLE SHEETS ==========
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Replace with your actual Google Sheet name
sheet = client.open("PC Activity Logger").sheet1

# ======== CLEAR SHEET AT START =========
sheet.clear()
sheet.append_row(["Time", "Process Name", "Window Title"])
sheet.update('D1', [['RUNNING']])  # Change to 'STOP' in Google Sheet to end script

# ========== TRACKING ==========
known_pids = set()

def get_active_window_title():
    """Get the active window title on Linux using xdotool"""
    try:
        window_id = subprocess.check_output(["xdotool", "getactivewindow"]).strip()
        if not window_id:
            return "N/A"
        window_name = subprocess.check_output(["xdotool", "getwindowname", window_id]).decode("utf-8").strip()
        return window_name
    except subprocess.CalledProcessError:
        return "N/A"
    except FileNotFoundError:
        return "xdotool not installed"

print("Monitoring started. Type 'STOP' in cell D1 on Google Sheet to halt.\n")

while True:
    # ======== CHECK FOR REMOTE STOP ========
    try:
        control_value = sheet.acell('D1').value.strip().upper()
        if control_value == "STOP":
            print("🛑 STOP command received from Google Sheet. Exiting...")
            break
    except Exception as e:
        print("⚠️ Could not check STOP signal:", e)

    # ======== CHECK FOR NEW PROCESSES ========
    for proc in psutil.process_iter(['pid', 'name']):
        pid = proc.info['pid']
        pname = proc.info['name']

        if pid not in known_pids:
            known_pids.add(pid)

            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            window_title = get_active_window_title()

            try:
                sheet.append_row([time_now, pname, window_title])
            except Exception as e:
                print("❌ Failed to write to Google Sheet:", e)

    time.sleep(3)  # Wait before next check
