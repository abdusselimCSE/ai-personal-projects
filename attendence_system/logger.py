import os
import csv
import requests
from datetime import datetime
import config

class AttendanceLogger:
    def __init__(self, log_path=config.LOG_PATH, cooldown=config.COOLDOWN_SECONDS):
        self.log_path = log_path
        self.cooldown = cooldown
        self.last_seen = {}  # {name: timestamp} for rapid UI cooldowns
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Creates the CSV file with headers if it doesn't exist."""
        if not os.path.exists(self.log_path):
            with open(self.log_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Date", "Time"])

    def log_attendance(self, name):
        """
        Logs the attendee. 
        Returns strings mapping to flutter states:
          "SUCCESS" (First time today)
          "ALREADY_LOGGED" (Google Sheet rejected as duplicate)
          "COOLDOWN" (Too rapid of a camera scan spam)
          "ERROR" (Network error)
        """
        if name == "Unknown":
            return "UNKNOWN"

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
            
        # Check rapid scan cooldown just in case (currently 0)
        if self.cooldown > 0:
            if name in self.last_seen:
                time_since_last = (now - self.last_seen[name]).total_seconds()
                if time_since_last < self.cooldown:
                    return "COOLDOWN"

        self.last_seen[name] = now
        
        # Sync to Google Sheets to Verify
        if hasattr(config, 'GOOGLE_SHEETS_URL') and config.GOOGLE_SHEETS_URL:
            try:
                payload = {"name": name, "date": date_str, "time": time_str}
                # Sync blocking request. We wait for Google Apps Script to reply.
                response = requests.post(config.GOOGLE_SHEETS_URL, json=payload, timeout=10)
                
                # The response will be either "SUCCESS" or "ALREADY_LOGGED"
                status = response.text.strip().upper()
                
                if status == "ALREADY_LOGGED":
                    print(f"📊 [Sheets] Rejected: {name} is already logged today.")
                    return "ALREADY_LOGGED"
                elif status == "SUCCESS":
                    print(f"🌐 [Sheets] Successfully synced {name} to Google Sheets!")
                else:
                    # In case of Apps Script breaking
                    print(f"⚠️ [Sheets] Unknown response: {status}")
                    return "ERROR"
            except Exception as e:
                print(f"⚠️ Failed to sync with Google Sheets: {e}")
                return "ERROR"
                
        # If successfully logged to Google Sheets, optionally append to local CSV as backup
        with open(self.log_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([name, date_str, time_str])
        
        print(f"✅ Logged local attendance for {name} at {time_str}")
        return "SUCCESS"
