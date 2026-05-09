"""Script to send daily reminders to all users"""
import os
import asyncio
import logging
from datetime import datetime
from telegram import Bot
from database import get_all_users, get_today_score
from config import TIMEZONE

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def send_reminders():
    """Send reminders to all users"""
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set")
        return

    bot = Bot(token=TOKEN)
    all_users = get_all_users()

    if not all_users:
        logger.info("No users to remind")
        return

    logger.info(f"Sending reminders to {len(all_users)} users")

    successful = 0
    failed = 0

    for chat_id in all_users:
        try:
            today_score = get_today_score(chat_id)

            if today_score:
                # User already scored today
                message = (
                    f"✅ **Bạn đã ghi điểm hôm nay**\n\n"
                    f"📊 Điểm: {today_score[0]}/10"
                )
                if today_score[1]:
                    message += f"\n📝 Ghi chú: {today_score[1][:100]}"
            else:
                # Remind user to score
                message = (
                    "⏰ **Nhắc nhở cập nhật điểm nỗ lực**\n\n"
                    "Hôm nay bạn có nỗ lực cho mục tiêu của đời bạn không?\n"
                    "Hãy tự chấm điểm nỗ lực của mình (từ 1-10).\n\n"
                    "Gửi /score để bắt đầu."
                )

            await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown'
            )
            successful += 1
            logger.info(f"Reminder sent to {chat_id}")

        except Exception as e:
            failed += 1
            logger.error(f"Failed to send reminder to {chat_id}: {e}")

    logger.info(f"Reminder complete - Sent: {successful}, Failed: {failed}")

async def main():
    """Main function"""
    logger.info("Starting reminder script")
    await send_reminders()
    logger.info("Reminder script finished")

if __name__ == '__main__':
    asyncio.run(main())
