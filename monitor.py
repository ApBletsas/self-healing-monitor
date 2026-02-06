import psutil
import shutil
import os
import logging
import requests
from logging.handlers import RotatingFileHandler

# -------------------------
# CONFIGURATION
# -------------------------
DISK_THRESHOLD = 10  # percent
LOG_FILE = "logs/system_monitor.log"
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/YOUR/WEBHOOK/HERE"

# Directories safe to clean on macOS
CLEANUP_PATHS = [
    "/tmp",
    os.path.expanduser("~/Library/Caches")
]

# -------------------------
# LOGGING SETUP WITH ROTATION
# -------------------------
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[handler]
)

# -------------------------
# HELPER FUNCTIONS
# -------------------------
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_disk_usage():
    disk = psutil.disk_usage("/")
    return disk.percent

def clean_temp_files():
    freed_space = 0
    for path in CLEANUP_PATHS:
        if os.path.exists(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        size = os.path.getsize(item_path)
                        os.remove(item_path)
                        freed_space += size
                    elif os.path.isdir(item_path):
                        size = shutil.disk_usage(item_path).used
                        shutil.rmtree(item_path)
                        freed_space += size
                except Exception as e:
                    logging.error(f"Failed to delete {item_path}: {e}")
    return freed_space / (1024 * 1024)  # MB

def send_slack_alert(message):
    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        logging.error(f"Slack notification failed: {e}")

# -------------------------
# MAIN LOGIC
# -------------------------
def main():
    cpu = get_cpu_usage()
    disk = get_disk_usage()

    logging.info(f"CPU Usage: {cpu}% | Disk Usage: {disk}%")

    if disk > (100 - DISK_THRESHOLD):
        logging.warning("Disk space critically low. Starting cleanup.")

        freed_mb = clean_temp_files()
        message = (
            f"Disk space low!\n"
            f"CPU: {cpu}%\n"
            f"Disk: {disk}%\n"
            f"Freed: {freed_mb:.2f} MB"
        )

        logging.info(f"Cleanup completed. Freed {freed_mb:.2f} MB")
        send_slack_alert(message)

if __name__ == "__main__":
    main()