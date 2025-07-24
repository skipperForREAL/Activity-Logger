import psutil
import win32gui
import time
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ========== SETUP GOOGLE SHEETS ==========
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# add the file with .json api credentials.json part
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Replace with your actual Google Sheet name
sheet = client.open("PC Activity Logger").sheet1

# ======== CLEAR SHEET AT START =========
# Clear all existing content in the sheet
sheet.clear()

# Re-add header row
sheet.append_row(["Time", "Process Name", "Window Title"])

# Create control cell for remote STOP
sheet.update('D1', [['RUNNING']])  # Change to 'STOP' to end script

# ========== TRACKING ==========
known_pids = set()

def get_active_window_title():
    """Get the title of the currently focused window"""
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return "N/A"

print("Monitoring started. Type 'STOP' in cell D1 on Google Sheet to halt.\n")

while True:
    # ========== CHECK FOR REMOTE STOP ==========
    try:
        control_value = sheet.acell('D1').value.strip().upper()
        if control_value == "STOP":
            print("🛑 STOP command received from Google Sheet. Exiting...")
            break
    except Exception as e:
        print("⚠️ Could not check STOP signal:", e)

    # ========== CHECK FOR NEW PROCESSES ==========
    for proc in psutil.process_iter(['pid', 'name']):
        pid = proc.info['pid']
        pname = proc.info['name']

        if pid not in known_pids:
            known_pids.add(pid)

            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            window_title = get_active_window_title()

            # Uncomment for debugging:
            # print(f"[{time_now}] {pname} | {window_title}")

            try:
                sheet.append_row([time_now, pname, window_title])
            except Exception as e:
                print("❌ Failed to write to Google Sheet:", e)

    time.sleep(3)  # Wait before next check
