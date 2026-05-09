#!/bin/bash
# Wrapper script for cron - runs remind.py safely

# ============ CONFIGURATION ============
# Update these paths for your setup
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="$APP_DIR/.env/bin/python3"
LOG_FILE="$APP_DIR/remind.log"

# ============ FALLBACK PATHS ============
# If using different venv location, update here:
# VENV_PYTHON="/usr/bin/python3"  # System Python
# VENV_PYTHON="/usr/local/bin/python3"  # Homebrew
# VENV_PYTHON="/opt/bot/daily-effort-logs/.env/bin/python3"  # Custom path

# ============ ENVIRONMENT ============
export PYTHONUNBUFFERED=1  # Unbuffered output
# export TELEGRAM_BOT_TOKEN="your_token"  # Uncomment and set if not in .env

# ============ EXECUTION ============
cd "$APP_DIR" || {
    echo "ERROR: Failed to cd to $APP_DIR" >> "$LOG_FILE" 2>&1
    exit 1
}

# Run Python script
"$VENV_PYTHON" remind.py >> "$LOG_FILE" 2>&1

# Log exit status
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "ERROR: remind.py exited with code $EXIT_CODE at $(date)" >> "$LOG_FILE" 2>&1
fi

exit $EXIT_CODE
