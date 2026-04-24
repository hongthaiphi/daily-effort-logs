# 🚀 Quick Start Guide

Hướng dẫn nhanh để chạy chatbot trong 5 phút.

## ✅ Bước 1: Tạo Telegram Bot Token

1. Mở Telegram → tìm **@BotFather**
2. Gửi `/newbot`
3. Đặt tên bot (ví dụ: "Effort Tracker Bot")
4. Đặt username (ví dụ: "my_effort_tracker_bot")
5. Copy **Bot Token** nhận được

## 📦 Bước 2: Cài đặt môi trường

```bash
# Clone/download code
cd effort-tracker-bot

# Tạo virtual environment (tuỳ chọn nhưng khuyến khích)
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate        # Windows

# Cài dependencies
pip install -r requirements.txt
```

## ⚙️ Bước 3: Cấu hình

### Cách 1: Dùng environment variable

**Linux/Mac:**
```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
python bot.py
```

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN="your-token-here"
python bot.py
```

### Cách 2: Tạo file `.env`

```bash
cp .env.example .env
```

Edit `.env`:
```
TELEGRAM_BOT_TOKEN=your-token-here
```

Thêm vào `bot.py` (dòng đầu):
```python
from dotenv import load_dotenv
load_dotenv()
```

Cài thêm:
```bash
pip install python-dotenv
```

## ▶️ Bước 4: Chạy bot

```bash
python bot.py
```

Nếu thấy `Bot started...`, tức là thành công!

## 🧪 Bước 5: Test bot

1. Mở Telegram
2. Tìm bot của bạn (@username-bot)
3. Gửi `/start`
4. Gửi `/score` để test

## 🌐 Bước 6: Deploy lên VPS (tuỳ chọn)

### Cách A: Systemd (khuyến khích)

```bash
# SSH vào VPS
ssh ubuntu@your-ip

# Download code
git clone your-repo
cd effort-tracker-bot
pip3 install -r requirements.txt

# Tạo systemd service
sudo nano /etc/systemd/system/effort-tracker.service
```

Paste nội dung:
```ini
[Unit]
Description=Effort Tracker Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/effort-tracker-bot
Environment="TELEGRAM_BOT_TOKEN=your-token"
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl daemon-reload
sudo systemctl enable effort-tracker
sudo systemctl start effort-tracker
sudo systemctl status effort-tracker
```

### Cách B: Docker

```bash
# Trên VPS
git clone your-repo
cd effort-tracker-bot

# Tạo .env
echo 'TELEGRAM_BOT_TOKEN=your-token' > .env

# Run
docker-compose up -d

# Check logs
docker-compose logs -f
```

## 🎮 Các lệnh bot

```
/start   → Xem danh sách lệnh
/score   → Ghi điểm hôm nay
/stats   → Xem thống kê
/chart   → Xem biểu đồ
/recent  → Xem nhật kí
/help    → Trợ giúp chi tiết
```

## 📁 Cấu trúc file

```
effort-tracker-bot/
├── bot.py                 ← Chương trình chính
├── database.py            ← SQLite operations
├── dashboard.py           ← Vẽ chart
├── config.py              ← Cấu hình tùy chỉnh
├── requirements.txt       ← Dependencies
├── Dockerfile             ← Docker config
├── docker-compose.yml     ← Docker compose
├── .env.example           ← Ví dụ .env
├── README.md              ← Tài liệu đầy đủ
├── QUICKSTART.md          ← File này
├── effort_tracker.db      ← Database (tự tạo)
└── charts/                ← Hình chart (tự tạo)
```

## ⚙️ Tùy chỉnh

### Thay đổi giờ nhắc nhở

Mở `config.py`:
```python
REMINDER_HOUR = 20      # 8 PM
REMINDER_MINUTE = 0
```

Thay `20` thành giờ mong muốn (0-23).

### Thay đổi timezone

```python
TIMEZONE = pytz.timezone('Asia/Ho_Chi_Minh')
```

Timezone khác: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

### Thay đổi khoảng thống kê

Mở `bot.py`, tìm `DEFAULT_STATS_DAYS`:
```python
stats = get_stats(user.id, 30)  # 30 → con số khác
```

## 🔍 Kiểm tra sự cố

### Bot không chạy
```bash
python bot.py  # Xem error message
```

### Bot không gửi nhắc nhở
- Kiểm tra timezone đúng không
- Kiểm tra bot đang chạy: `ps aux | grep bot.py`

### Database bị lỗi
```bash
rm effort_tracker.db
# Bot sẽ tạo database mới
```

## 💡 Tips

- Lần đầu chạy, bot sẽ tự tạo `effort_tracker.db`
- Database tự động lưu mọi user & điểm số
- Chart tự động tạo trong thư mục `charts/`
- Dùng `screen` hoặc `nohup` để bot chạy background

```bash
# Chạy background với screen
screen -S effort-bot
python bot.py
# Ctrl+A, Ctrl+D để thoát (bot vẫn chạy)

# Quay lại: screen -r effort-bot
```

## 📚 Tài liệu đầy đủ

Xem `README.md` để hướng dẫn chi tiết.

---

**Chúc bạn thành công! 💪**
