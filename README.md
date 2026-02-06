# Self-Healing Server Monitor

A self-healing server monitor that checks CPU and disk usage every 5 minutes. Automatically cleans temporary files when disk space is critically low, logs all activity and sends Slack notifications.
Made it on Mac OS.

---

## Features

- Monitors CPU and disk usage
- Automatically cleans safe temp directories (`/tmp` and `~/Library/Caches`)
- Logs activity and errors with log rotation
- Sends Slack alerts when disk space is critically low
- Fully compatible with macOS + Python 3.12.2 via pyenv

---

## Setup Instructions

1. Clone this repo:

```bash
git clone <YOUR_REPO_URL>
cd self-healing-monitor
```

2. Set Python version using pyenv:

```bash
pyenv install 3.12.2   # if not installed
pyenv local 3.12.2
```

3. Create a virtual environment: 

```bash
python -m venv venv
source venv/bin/activate
```

4. Install dependencies: 

```bash
pip install -r requirements.txt
```

5. Configure Slack webhook in monitor.py:

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/..."

6. Run manually:

```bash
python monitor.py
```

7. If you want you can also schedule it to execute automatically every 5min using cron:

```bash
crontab -e
# add:
*/5 * * * * /full/path/to/venv/bin/python /full/path/to/monitor.py
```

--

## License 

This project is licensed under the MIT License
