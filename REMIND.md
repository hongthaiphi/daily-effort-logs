# Reminder Script - remind.py

Script này gửi tin nhắn nhắc nhở tới tất cả người dùng của bot, yêu cầu cập nhật điểm nỗ lực hàng ngày.

## Tính năng

- ✅ Gửi nhắc nhở tới **tất cả người dùng** của bot
- 📊 Kiểm tra xem người dùng đã ghi điểm hôm nay chưa
  - Nếu **chưa**: gửi lời nhắc nhở ghi điểm
  - Nếu **rồi**: gửi tin nhắn xác nhận với điểm hiện tại
- 🛡️ Xử lý lỗi tự động, báo log chi tiết
- 📝 Ghi log số lượng tin nhắn gửi thành công/thất bại

## Cách sử dụng

### 1. Chạy thủ công (Manual Run)

```bash
python remind.py
```

### 2. Chạy hàng ngày qua Cron (Linux/Mac) - ✅ RECOMMENDED

**Sử dụng wrapper script** (an toàn, xử lý virtual environment tự động):

```bash
crontab -e
```

Thêm dòng này để chạy lúc **8:00 AM** hàng ngày:
```cron
0 8 * * * /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh
```

**Hoặc** để chạy vào **20:00 (8 PM)**:
```cron
0 20 * * * /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh
```

👉 **Chi tiết setup:** xem [CRON_SETUP.md](CRON_SETUP.md)

### 3. Chạy hàng ngày qua Docker

Nếu sử dụng Docker, thêm service riêng trong `docker-compose.yml`:

```yaml
reminder:
  build: .
  environment:
    - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
  volumes:
    - ./effort_tracker.db:/app/effort_tracker.db
  command: python remind.py
  restart: no
```

Sau đó tạo cron job trên host chạy:
```bash
docker-compose -f /path/to/docker-compose.yml run reminder
```

### 4. Tích hợp vào Bot (tùy chọn)

Nếu muốn chạy reminder tách biệt từ bot chính:
- Bot chạy trên port 8000 (ví dụ)
- Cron job chạy `python remind.py` hàng ngày
- Đảm bảo cùng sử dụng database `effort_tracker.db`

## Tin nhắn gửi đi

### Nếu người dùng chưa ghi điểm:
```
⏰ **Nhắc nhở cập nhật điểm nỗ lực**

Hôm nay bạn có nỗ lực cho mục tiêu của đời bạn không?
Hãy tự chấm điểm nỗ lực của mình (từ 1-10).

Gửi /score để bắt đầu.
```

### Nếu người dùng đã ghi điểm:
```
✅ **Bạn đã ghi điểm hôm nay**

📊 Điểm: 8/10
📝 Ghi chú: Hoàn thành dự án...
```

## Environment Variables

Đảm bảo đã set:
```bash
export TELEGRAM_BOT_TOKEN="your_token_here"
```

## Log Files

Log được lưu tại:
- Terminal: hiển thị trực tiếp
- File: `remind.log` (nếu redirect qua cron job)

Xem log:
```bash
tail -f remind.log
```

## Troubleshooting

### Error: "TELEGRAM_BOT_TOKEN environment variable not set"
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
```

### Error: "database is locked"
- Đảm bảo bot chính không đang chạy hoặc không đang ghi database
- Chạy reminder lúc bot rảnh (ví dụ: 2 AM)

### Một số người dùng không nhận được tin nhắn
- Kiểm tra log xem lỗi gì
- Người dùng có thể đã block bot hoặc bị chặn
- Log sẽ hiển thị `Failed to send reminder to [chat_id]`

## Tùy chỉnh

Chỉnh sửa `remind.py` để:
- Thay đổi nội dung tin nhắn
- Thêm emoji khác
- Thay đổi define thời gian kiểm tra (dùng timezone)
