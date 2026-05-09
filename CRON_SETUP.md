# 🕐 Cài đặt Cron Job với run_remind_cron.sh

## Tập tin mới

**File:** `run_remind_cron.sh`
- Wrapper script an toàn cho cron
- Tự động tìm paths
- Ghi log đầy đủ
- Xử lý lỗi

## ✅ Cách setup (Chi tiết)

### Bước 1: Cập nhật file (nếu cần)

Mở `run_remind_cron.sh` và kiểm tra:
```bash
nano run_remind_cron.sh
```

Nếu virtual environment ở chỗ khác, chỉnh sửa:
```bash
VENV_PYTHON="$APP_DIR/.env/bin/python3"
```

Nếu không có venv, dùng system Python:
```bash
VENV_PYTHON="/usr/bin/python3"
```

### Bước 2: Test script trước

```bash
cd /Users/phihongthai/Documents/claude/telegrambotEffort
./run_remind_cron.sh
```

Kiểm tra log:
```bash
tail -f remind.log
```

### Bước 3: Thêm vào crontab

```bash
crontab -e
```

Thêm dòng này (chạy 8 AM mỗi ngày):
```cron
0 8 * * * /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh
```

**Hoặc các thời gian khác:**
```cron
# 8 PM hàng ngày
0 20 * * * /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh

# 8 AM + 8 PM
0 8,20 * * * /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh

# Mỗi 6 tiếng
0 */6 * * * /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh
```

### Bước 4: Xác minh cron job

```bash
# List cron jobs
crontab -l

# Watch logs
tail -f /Users/phihongthai/Documents/claude/telegrambotEffort/remind.log
```

## 🔧 Configuration

### Token từ environment variable

```bash
export TELEGRAM_BOT_TOKEN="your_token"
crontab -e
```

Hoặc thêm vào shell profile (.bashrc, .zshrc):
```bash
export TELEGRAM_BOT_TOKEN="your_token"
```

### Token từ .env file

Chỉnh sửa `run_remind_cron.sh` bỏ comment này:
```bash
# export TELEGRAM_BOT_TOKEN="your_token"  # Uncomment and set
```

Thành:
```bash
export TELEGRAM_BOT_TOKEN="your_token"
```

**Hoặc** tạo file `.env` trong thư mục:
```bash
echo "TELEGRAM_BOT_TOKEN=your_token" > .env
```

Cập nhật `remind.py` thêm dòng:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 🐛 Troubleshooting

### Kiểm tra macOS cron log

```bash
log stream --predicate 'process == "cron"' --level debug
```

### Kiểm tra Linux cron log

```bash
sudo journalctl -u cron --since today
sudo tail -f /var/log/cron
```

### Nếu cron không chạy

1. **Kiểm tra tệp permissions:**
   ```bash
   ls -la /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh
   # Phải có 'x' (executable)
   ```

2. **Kiểm tra Python path:**
   ```bash
   /Users/phihongthai/Documents/claude/telegrambotEffort/.env/bin/python3 --version
   ```

3. **Kiểm tra database:**
   ```bash
   ls -la /Users/phihongthai/Documents/claude/telegrambotEffort/effort_tracker.db
   ```

4. **Test thủ công:**
   ```bash
   /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh
   tail remind.log
   ```

## 📝 Log file

Tất cả output (success/error) được ghi tại:
```
/Users/phihongthai/Documents/claude/telegrambotEffort/remind.log
```

Xem realtime:
```bash
tail -f /Users/phihongthai/Documents/claude/telegrambotEffort/remind.log
```

## ✨ Ưu điểm của wrapper script

✅ Không cần `source` virtual environment  
✅ Tự động tìm paths (relative path)  
✅ Full error logging  
✅ Exit code handling  
✅ PYTHONUNBUFFERED cho output tốt hơn  
✅ Dễ tùy chỉnh  

## 🎯 Quick Reference

```bash
# Test
./run_remind_cron.sh

# View logs
tail -f remind.log

# Setup cron
crontab -e
# Add: 0 8 * * * /Users/phihongthai/Documents/claude/telegrambotEffort/run_remind_cron.sh

# Check cron
crontab -l
```
