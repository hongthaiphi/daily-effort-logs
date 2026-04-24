"""Main Telegram Bot - Effort Tracker"""
import os
from datetime import datetime
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    filters, ContextTypes, ConversationHandler
)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz

from database import (
    init_db, add_user, get_user_id, save_score, get_today_score,
    get_scores_range, get_stats, get_all_users
)
from dashboard import create_chart

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# States for conversation
SCORE_INPUT, DIARY_INPUT = range(2)

# Bot token - set this as environment variable
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')  # Vietnam timezone

class EffortTrackerBot:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        add_user(user.id, user.username, user.first_name)

        await update.message.reply_text(
            f"👋 Xin chào {user.first_name}!\n\n"
            "Tôi là bot ghi nhận nỗ lực hàng ngày của bạn.\n\n"
            "Hàng ngày lúc 8h tối, tôi sẽ hỏi bạn tự chấm điểm nỗ lực "
            "(từ 1-10 điểm).\n\n"
            "Các lệnh có sẵn:\n"
            "/score - Ghi điểm hôm nay\n"
            "/stats - Xem thống kê\n"
            "/chart - Xem biểu đồ\n"
            "/recent - Xem nhật kí gần đây\n"
            "/help - Trợ giúp"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **Hướng dẫn sử dụng:**

**/score** - Ghi điểm nỗ lực hôm nay
Bạn sẽ được yêu cầu nhập điểm từ 1-10

**/stats** - Xem thống kê
Hiển thị: điểm trung bình, cao nhất, thấp nhất trong 30 ngày

**/chart** - Xem biểu đồ
Vẽ biểu đồ đường thể hiện điểm nỗ lực qua các ngày

**/recent** - Xem nhật kí gần đây
Hiển thị 10 ngày gần nhất cùng ghi chú

**/help** - Hiển thị trợ giúp này

💡 **Mẹo:**
- Ghi điểm xong, bạn có thể thêm nhật kí ngắn (diary)
- Điểm từ 1-10: 1 = không nỗ lực, 10 = nỗ lực cực đại
- Bạn có thể cập nhật điểm của ngày hôm nay lúc nào cũng được
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def score_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /score command - start conversation"""
        user = update.effective_user
        add_user(user.id, user.username, user.first_name)

        today_score = get_today_score(user.id)
        if today_score:
            current_text = f"\n\nCó ghi chú: {today_score[1][:50]}..." if today_score[1] else ""
            await update.message.reply_text(
                f"📊 Điểm hôm nay: {today_score[0]}/10{current_text}\n\n"
                "Nhập điểm mới (1-10) để cập nhật, hoặc /cancel để thoát:"
            )
        else:
            await update.message.reply_text(
                "Hôm nay bạn có nỗ lực cho mục tiêu của đời bạn không?\n\n"
                "Vui lòng tự chấm điểm nỗ lực của mình (1-10):"
            )

        return SCORE_INPUT

    async def receive_score(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle score input"""
        try:
            score = int(update.message.text)
            if score < 1 or score > 10:
                await update.message.reply_text("❌ Vui lòng nhập số từ 1 đến 10")
                return SCORE_INPUT

            context.user_data['score'] = score
            await update.message.reply_text(
                f"✅ Điểm nỗ lực: {score}/10\n\n"
                "Bây giờ, bạn muốn ghi một ghi chú ngắn không? "
                "(Gửi ghi chú hoặc gửi /skip để bỏ qua)"
            )
            return DIARY_INPUT

        except ValueError:
            await update.message.reply_text("❌ Vui lòng nhập một số (1-10)")
            return SCORE_INPUT

    async def receive_diary(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle diary input"""
        score = context.user_data['score']
        diary = update.message.text if update.message.text != "/skip" else ""

        save_score(update.effective_user.id, score, diary)

        response = f"🎯 Lưu thành công!\n\nĐiểm: {score}/10"
        if diary and diary != "/skip":
            response += f"\nGhi chú: {diary}"

        await update.message.reply_text(response)
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel conversation"""
        await update.message.reply_text("❌ Hủy bỏ. Gửi /score để thử lại.")
        return ConversationHandler.END

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command"""
        user = update.effective_user
        stats = get_stats(user.id, 30)

        if not stats['total_days']:
            await update.message.reply_text("📊 Chưa có dữ liệu. Hãy ghi điểm trước!")
            return

        text = (
            f"📊 **Thống kê 30 ngày gần đây**\n\n"
            f"📈 Điểm trung bình: {stats['avg_score']}/10\n"
            f"🔝 Điểm cao nhất: {stats['max_score']}/10\n"
            f"🔻 Điểm thấp nhất: {stats['min_score']}/10\n"
            f"📅 Tổng ngày ghi: {stats['total_days']} ngày"
        )
        await update.message.reply_text(text, parse_mode='Markdown')

    async def chart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /chart command - generate and send chart"""
        user = update.effective_user
        scores = get_scores_range(user.id, 30)

        if not scores:
            await update.message.reply_text("📊 Chưa có dữ liệu để vẽ biểu đồ")
            return

        chart_path = create_chart(user.id, scores)

        with open(chart_path, 'rb') as chart_file:
            await update.message.reply_photo(
                photo=chart_file,
                caption="📊 Biểu đồ nỗ lực 30 ngày gần đây"
            )

    async def recent_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /recent command"""
        user = update.effective_user
        scores = get_scores_range(user.id, 10)

        if not scores:
            await update.message.reply_text("📔 Chưa có ghi chú nào")
            return

        text = "📔 **Nhật kí gần đây (10 ngày)**\n\n"
        for date, score, diary in scores:
            text += f"📅 {date}: {score}/10\n"
            if diary:
                text += f"   📝 {diary}\n"
            text += "\n"

        await update.message.reply_text(text, parse_mode='Markdown')

    async def daily_reminder(self, context: ContextTypes.DEFAULT_TYPE):
        """Send daily reminder at 8 PM"""
        all_users = get_all_users()

        for chat_id in all_users:
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=(
                        "⏰ **Thời gian ghi nhận nỗ lực hàng ngày**\n\n"
                        "Hôm nay bạn có nỗ lực cho mục tiêu của đời bạn không?\n"
                        "Hãy tự chấm điểm nỗ lực của mình (từ 1-10).\n\n"
                        "Gửi /score để bắt đầu."
                    ),
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Failed to send reminder to {chat_id}: {e}")

    def setup_scheduler(self, app: Application):
        """Setup APScheduler for daily reminders"""
        # Schedule daily reminder at 8 PM Vietnam time
        self.scheduler.add_job(
            self.daily_reminder,
            CronTrigger(hour=20, minute=0, timezone=TIMEZONE),
            args=[app],
            id='daily_reminder',
            replace_existing=True
        )

        self.scheduler.start()
        logger.info("Scheduler started - daily reminder at 8 PM")

def main():
    """Start the bot"""
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")

    # Initialize database
    init_db()
    logger.info("Database initialized")

    # Create application
    application = Application.builder().token(TOKEN).build()

    # Create bot instance
    bot = EffortTrackerBot()

    # Setup scheduler
    bot.setup_scheduler(application)

    # Commands
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("stats", bot.stats_command))
    application.add_handler(CommandHandler("chart", bot.chart_command))
    application.add_handler(CommandHandler("recent", bot.recent_command))

    # Conversation handler for /score
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("score", bot.score_command)],
        states={
            SCORE_INPUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.receive_score)],
            DIARY_INPUT: [MessageHandler(filters.TEXT, bot.receive_diary)],
        },
        fallbacks=[CommandHandler("cancel", bot.cancel)],
    )
    application.add_handler(conv_handler)

    # Start bot
    logger.info("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    main()
