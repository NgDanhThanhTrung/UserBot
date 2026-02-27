import os
import asyncio
import logging
import time
import random
from fastapi import FastAPI, Path
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
from dotenv import load_dotenv

load_dotenv() [cite: 2]

# --- Cấu hình Logging ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s') [cite: 1]
logger = logging.getLogger(__name__)

app = FastAPI(title="Userbot Hybrid System")

# --- Cấu hình Mục tiêu cố định ---
TARGET_1 = "Yuicsa_bot"            # Mục tiêu cho lệnh điểm danh 
TARGET_2 = "deptraikhongsoai_bot"   # Mục tiêu cho lệnh spam

# --- Biến môi trường ---
API_ID = int(os.environ.get("API_ID", 0)) [cite: 1, 2]
API_HASH = os.environ.get("API_HASH", "") [cite: 1, 2]
# Tự động lấy session từ một trong hai biến có sẵn
SESSION_STR = os.environ.get("SESSION_STR") or os.environ.get("SESSION_STRING", "") [cite: 1, 2]

# Trạng thái điều khiển máy chủ
spam_control = {
    "is_running": False,
    "stop_flag": False,
    "count": 0
}
status_dd = {"last_sent": "Chưa gửi", "count": 0}

# Khởi tạo Telegram Client duy nhất
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH) [cite: 1, 2]

async def run_spam_task(base_cmd: str):
    """Tiến trình gửi 300 tin nhắn ngầm tới @deptraikhongsoai_bot"""
    global spam_control
    
    if spam_control["is_running"]:
        return

    spam_control["is_running"] = True
    spam_control["stop_flag"] = False
    spam_control["count"] = 0

    try:
        if not client.is_connected():
            await client.connect() [cite: 1, 2]

        while spam_control["count"] < 300: [cite: 2]
            # Lệnh /stop sẽ bật cờ này để máy chủ ngừng gửi tin
            if spam_control["stop_flag"]:
                logger.info(f"Dừng khẩn cấp tại tin {spam_control['count']}/300") [cite: 2]
                break

            msg = f"{base_cmd} #{spam_control['count']+1} - {time.strftime('%H:%M:%S')}" [cite: 2]
            await client.send_message(TARGET_2, msg) 
            
            spam_control["count"] += 1
            # Nghỉ ngẫu nhiên từ 1.2s - 3.5s để tránh bị Telegram khóa [cite: 2]
            await asyncio.sleep(random.uniform(1.2, 3.5))

    except FloodWaitError as e: [cite: 2]
        logger.warning(f"Flood wait {e.seconds}s. Đang chờ...") [cite: 2]
        await asyncio.sleep(e.seconds + 15) [cite: 2]
    except Exception as e:
        logger.error(f"Lỗi: {e}") [cite: 1, 2]
    finally:
        spam_control["is_running"] = False
        spam_control["stop_flag"] = False

# --- API Endpoints ---

@app.get("/")
async def root():
    return {
        "status": "Online ✅",
        "spam_status": "Chạy" if spam_control["is_running"] else "Nghỉ",
        "progress": f"{spam_control['count']}/300"
    }

@app.get("/health")
async def health():
    """Dùng để ping giữ server sống, KHÔNG gửi tin nhắn"""
    return {"status": "healthy"} [cite: 1, 2]

@app.get("/diemdanhapple")
async def diemdanh():
    """Gửi duy nhất 1 tin tới @Yuicsa_bot"""
    try:
        if not client.is_connected(): await client.connect()
        await client.send_message(TARGET_1, "/diemdanhapple") [cite: 1]
        
        status_dd["count"] += 1
        status_dd["last_sent"] = time.strftime('%H:%M:%S %d-%m-%Y') [cite: 1]
        return {"status": "Success", "target": TARGET_1}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}

@app.get("/stop")
async def stop_server_task():
    """Lệnh đề nghị máy chủ ngừng gửi tin nhắn ngay lập tức"""
    if spam_control["is_running"]:
        spam_control["stop_flag"] = True [cite: 2]
        return {"status": "Đã gửi lệnh STOP tới máy chủ."} [cite: 2]
    return {"status": "Không có task nào đang chạy."}

@app.get("/{command}")
async def start_spam(command: str = Path(...)):
    """Mọi lệnh khác sẽ bắt đầu spam tới @deptraikhongsoai_bot"""
    if command in ["favicon.ico", "health", "diemdanhapple", "stop"]:
        return
    
    full_cmd = f"/{command.replace('-', ' ')}" [cite: 2]
    asyncio.create_task(run_spam_task(full_cmd)) [cite: 2]
    return {"status": "Started", "target": TARGET_2, "cmd": full_cmd}

@app.on_event("startup")
async def startup_event():
    await client.connect() [cite: 1]
    logger.info("Bot Server đã sẵn sàng.") [cite: 1]
