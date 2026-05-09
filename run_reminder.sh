#!/bin/bash
# Script to run daily reminders

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Telegram Bot - Daily Reminder${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo -e "${RED}❌ Error: TELEGRAM_BOT_TOKEN is not set${NC}"
    echo "Set it with: export TELEGRAM_BOT_TOKEN='your_token'"
    exit 1
fi

echo -e "${GREEN}✓ Token configured${NC}"

# Check if database exists
if [ ! -f "$SCRIPT_DIR/effort_tracker.db" ]; then
    echo -e "${RED}❌ Error: Database not found${NC}"
    echo "Run the main bot first to create the database"
    exit 1
fi

echo -e "${GREEN}✓ Database found${NC}"

# Run the reminder script
echo -e "${BLUE}→ Starting reminder script...${NC}"
cd "$SCRIPT_DIR"

python3 remind.py

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Reminder script completed${NC}"
echo -e "${BLUE}========================================${NC}"
