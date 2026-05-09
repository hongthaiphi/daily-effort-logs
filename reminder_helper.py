"""Helper functions for reminder system"""
import os
import asyncio
import logging
from typing import List, Tuple
from telegram import Bot
from database import get_all_users, get_today_score

logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

class ReminderHelper:
    """Helper class for sending reminders"""

    def __init__(self):
        self.bot = Bot(token=TOKEN)

    async def send_to_all(self, filter_type: str = "all") -> Tuple[int, int]:
        """
        Send reminders to users based on filter type

        Args:
            filter_type: "all" | "not_scored" | "scored"
                - "all": Send to everyone (show status)
                - "not_scored": Send only to users who haven't scored today
                - "scored": Send only to users who already scored today

        Returns:
            Tuple of (successful, failed) count
        """
        all_users = get_all_users()

        if not all_users:
            logger.info("No users to remind")
            return 0, 0

        users_to_send = self._filter_users(all_users, filter_type)

        logger.info(f"Sending reminders to {len(users_to_send)} users (filter: {filter_type})")

        successful = 0
        failed = 0

        for chat_id in users_to_send:
            try:
                message = self._build_message(chat_id)
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
                successful += 1
                logger.info(f"✓ Sent to {chat_id}")

            except Exception as e:
                failed += 1
                logger.error(f"✗ Failed to send to {chat_id}: {e}")

        logger.info(f"Summary - Sent: {successful}, Failed: {failed}")
        return successful, failed

    def _filter_users(self, users: List[int], filter_type: str) -> List[int]:
        """Filter users based on whether they've scored today"""
        if filter_type == "all":
            return users
        elif filter_type == "not_scored":
            return [u for u in users if not get_today_score(u)]
        elif filter_type == "scored":
            return [u for u in users if get_today_score(u)]
        else:
            logger.warning(f"Unknown filter type: {filter_type}, using 'all'")
            return users

    def _build_message(self, chat_id: int) -> str:
        """Build appropriate message based on user's status"""
        today_score = get_today_score(chat_id)

        if today_score:
            message = (
                f"✅ **Bạn đã ghi điểm hôm nay**\n\n"
                f"📊 Điểm: {today_score[0]}/10"
            )
            if today_score[1]:
                message += f"\n📝 Ghi chú: {today_score[1][:100]}"
        else:
            message = (
                "⏰ **Nhắc nhở cập nhật điểm nỗ lực**\n\n"
                "Hôm nay bạn có nỗ lực cho mục tiêu của đời bạn không?\n"
                "Hãy tự chấm điểm nỗ lực của mình (từ 1-10).\n\n"
                "Gửi /score để bắt đầu."
            )

        return message

    async def get_stats(self) -> dict:
        """Get reminder statistics"""
        all_users = get_all_users()
        scored_today = sum(1 for u in all_users if get_today_score(u))

        return {
            'total_users': len(all_users),
            'scored_today': scored_today,
            'not_scored': len(all_users) - scored_today,
            'score_rate': round((scored_today / len(all_users) * 100), 1) if all_users else 0
        }

async def main():
    """Example usage"""
    logging.basicConfig(level=logging.INFO)

    helper = ReminderHelper()

    # Show stats
    stats = await helper.get_stats()
    print(f"\n📊 Reminder Statistics:")
    print(f"  Total users: {stats['total_users']}")
    print(f"  Scored today: {stats['scored_today']}")
    print(f"  Not scored: {stats['not_scored']}")
    print(f"  Score rate: {stats['score_rate']}%\n")

if __name__ == '__main__':
    asyncio.run(main())
