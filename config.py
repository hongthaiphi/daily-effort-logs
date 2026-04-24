"""Configuration file - easily customize bot settings"""
import os
import pytz

# ============ TELEGRAM SETTINGS ============
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# ============ DATABASE SETTINGS ============
DB_PATH = "effort_tracker.db"

# ============ SCHEDULER SETTINGS ============
TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')  # Change to your timezone

# Daily reminder time (24-hour format)
REMINDER_HOUR = 20      # 8 PM
REMINDER_MINUTE = 0

# ============ EFFORT SCORE SETTINGS ============
MIN_SCORE = 1
MAX_SCORE = 10

# ============ STATISTICS SETTINGS ============
DEFAULT_STATS_DAYS = 30  # Default period for statistics
DEFAULT_CHART_DAYS = 30  # Default period for chart
RECENT_ENTRIES = 10     # Number of recent entries to show

# ============ CHART SETTINGS ============
CHART_WIDTH = 12
CHART_HEIGHT = 6
CHART_DPI = 100
CHARTS_DIR = "charts"

# ============ LOG SETTINGS ============
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# ============ VALIDATION ============
def validate_config():
    """Validate configuration"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    if MIN_SCORE >= MAX_SCORE:
        raise ValueError("MIN_SCORE must be less than MAX_SCORE")
    if REMINDER_HOUR < 0 or REMINDER_HOUR > 23:
        raise ValueError("REMINDER_HOUR must be between 0 and 23")
    if REMINDER_MINUTE < 0 or REMINDER_MINUTE > 59:
        raise ValueError("REMINDER_MINUTE must be between 0 and 59")
