# 🎯 Effort Tracker - Telegram Bot

Bot Telegram để ghi nhận và theo dõi nỗ lực hàng ngày. Hàng ngày lúc 8h tối, bot sẽ gửi câu hỏi yêu cầu bạn tự chấm điểm nỗ lực (1-10), lưu lại, và vẽ dashboard cá nhân.

## 🎨 Tính năng

✅ **Ghi điểm nỗ lực hàng ngày** (1-10 điểm)  
✅ **Ghi nhật kí/ghi chú ngắn** cùng với mỗi điểm  
✅ **Nhắc nhở tự động** lúc 8h tối mỗi ngày  
✅ **Biểu đồ đường** hiển thị xu hướng nỗ lực  
✅ **Thống kê 30 ngày**: trung bình, cao nhất, thấp nhất  
✅ **Xem lại nhật kí gần đây**  
✅ **SQLite database** - lưu dữ liệu cá nhân  

## 📋 Yêu cầu

- Python 3.8+
- Telegram Bot Token (tạo qua BotFather)
- VPS hoặc máy tính để chạy bot 24/7

## 🚀 Setup & Cài đặt

### 1️⃣ Clone/Download code

```bash
git clone <repo-url>
cd effort-tracker-bot
```

### 2️⃣ Tạo Telegram Bot

1. Mở Telegram, tìm **@BotFather**
2. Gửi `/newbot` và làm theo hướng dẫn
3. Sao chép **Bot Token** (ví dụ: `123456789:ABCdefGHIjkLMNOpqrSTUvwxYZ`)

### 3️⃣ Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set environment variable

**Trên Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token-here"
```

**Trên Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN="your-bot-token-here"
```

**Hoặc tạo file `.env`:**
```
TELEGRAM_BOT_TOKEN=your-bot-token-here
```

Sau đó cập nhật `bot.py`:
```python
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
```

Cài dotenv: `pip install python-dotenv`

### 5️⃣ Chạy bot (Local test)

```bash
python bot.py
```

Khi thấy "Bot started...", bot đã sẵn sàng. Mở Telegram tìm bot của bạn và gửi `/start`.

## 🌐 Deploy trên VPS (AWS/DigitalOcean)

### Tùy chọn 1: Chạy trực tiếp

```bash
# SSH vào VPS
ssh root@your-vps-ip

# Clone code
git clone <repo-url>
cd effort-tracker-bot

# Cài dependencies
pip3 install -r requirements.txt

# Set token
export TELEGRAM_BOT_TOKEN="your-token"

# Chạy bot (dùng nohup hoặc screen)
nohup python3 bot.py > bot.log 2>&1 &
```

### Tùy chọn 2: Dùng systemd (khuyến nghị)

Tạo file `/etc/systemd/system/effort-tracker.service`:

```ini
[Unit]
Description=Effort Tracker Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/effort-tracker-bot
Environment="TELEGRAM_BOT_TOKEN=your-token-here"
ExecStart=/usr/bin/python3 /home/ubuntu/effort-tracker-bot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable & start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable effort-tracker
sudo systemctl start effort-tracker

# Check status
sudo systemctl status effort-tracker

# View logs
sudo journalctl -u effort-tracker -f
```

### Tùy chọn 3: Docker (nếu VPS hỗ trợ)

Tạo `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
```

Build & run:
```bash
docker build -t effort-tracker .
docker run -e TELEGRAM_BOT_TOKEN="your-token" effort-tracker
```

## 📱 Hướng dẫn sử dụng

### Lệnh chính

| Lệnh | Chức năng |
|------|---------|
| `/start` | Khởi động, xem tất cả lệnh |
| `/score` | Ghi điểm nỗ lực hôm nay |
| `/stats` | Xem thống kê 30 ngày |
| `/chart` | Xem biểu đồ đường |
| `/recent` | Xem nhật kí gần đây (10 ngày) |
| `/help` | Trợ giúp chi tiết |

### Ví dụ quy trình sử dụng

1. **Nhận nhắc nhở lúc 8h tối**: Bot tự động gửi thông báo
2. **Gửi `/score`**: Nhập điểm (1-10)
3. **Viết ghi chú**: Ví dụ "Hôm nay code 5 giờ, tập gym 30p"
4. **Xem tiến độ**: Dùng `/chart` để thấy biểu đồ
5. **Theo dõi**: Mỗi ngày tiếp tục ghi điểm

## 📊 Cấu trúc dữ liệu

**SQLite Database: `effort_tracker.db`**

```
users
├── user_id (INT, PRIMARY KEY)
├── chat_id (INT, UNIQUE)
├── username
├── first_name
└── created_at (TIMESTAMP)

daily_scores
├── id (INT, PRIMARY KEY)
├── user_id (INT, FOREIGN KEY)
├── date (DATE)
├── score (INT, 1-10)
├── diary (TEXT)
└── created_at (TIMESTAMP)
```

## 🔧 Cấu hình

### Thay đổi giờ nhắc nhở

Trong `bot.py`, dòng 224:
```python
CronTrigger(hour=20, minute=0, timezone=TIMEZONE)  # 8h tối = 20:00
```

Thay `hour=20, minute=0` bằng giờ mong muốn.

### Thay đổi timezone

```python
TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')  # Đổi thành timezone của bạn
```

Danh sách timezone: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

### Thay đổi khoảng thời gian thống kê

Trong `bot.py`, các hàm `stats_command`, `chart_command`:
```python
stats = get_stats(user.id, 30)  # 30 ngày, đổi thành con số khác
```

## 🔔 Hệ thống Reminder (Nhắc nhở)

Bot có hệ thống nhắc nhở tự động và manual:

### Reminder tự động (trong bot)
Bot tự động gửi nhắc nhở lúc **8h tối** mỗi ngày tới tất cả người dùng.

### Reminder Manual (remind.py)
Script `remind.py` cho phép gửi nhắc nhở theo yêu cầu:

**Chạy thủ công:**
```bash
python remind.py
```

**Chạy qua Cron (Linux/Mac):**
```bash
crontab -e
# Thêm dòng này để chạy lúc 8 AM hàng ngày:
0 8 * * * cd /path/to/bot && /usr/bin/python3 remind.py >> remind.log 2>&1
```

**Hoặc dùng shell script:**
```bash
./run_reminder.sh
```

Xem chi tiết: [REMIND.md](REMIND.md)

**Tính năng:**
- Gửi tới tất cả người dùng
- Kiểm tra xem người dùng đã ghi điểm chưa
- Nếu chưa: gửi lời nhắc nhở
- Nếu rồi: xác nhận với điểm hiện tại
- Ghi log chi tiết (successful/failed)

## 🐛 Khắc phục sự cố

### Bot không gửi nhắc nhở

- Kiểm tra bot đang chạy: `ps aux | grep bot.py`
- Kiểm tra logs: `tail -f bot.log`
- Kiểm tra timezone hệ thống: `timedatectl` (Linux)

### Database bị khóa (locked)

```bash
rm effort_tracker.db
# Bot sẽ tạo database mới
```

### Bot không nhận lệnh

- Đảm bảo bot token đúng
- Kiểm tra bot có được thêm vào chat chưa
- Restart bot: `systemctl restart effort-tracker`

## 📈 Mở rộng tính năng

**Ideas:**
- Thêm tính năng "streak" (chuỗi ngày liên tiếp)
- Thêm mục tiêu (goals) dài hạn
- Tính toán xu hướng (trending up/down)
- Gửi báo cáo hàng tuần
- Chia sẻ với bạn bè (leaderboard)
- Lưu backup tự động lên cloud

## 📝 License

MIT License

## 📧 Support

Nếu có vấn đề, tạo issue hoặc liên hệ.

---

**Made with 💪 for daily effort tracking**
