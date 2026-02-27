import os
import asyncio
import logging
import time
import random
from fastapi import FastAPI, Path
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Userbot Hybrid - Render")

# --- Cấu hình Mục tiêu cố định ---
TARGET_1 = "Yuicsa_bot"            # Mục tiêu cho lệnh điểm danh
TARGET_2 = "deptraikhongsoai_bot"   # Mục tiêu cho work, daily và spam 300 tin

# --- Thông tin API ---
API_ID = 39516756
API_HASH = "02b3f7dfef549f670c3eb938912754c8"
SESSION_STR = os.environ.get("SESSION_STR", "")

# Trạng thái điều khiển máy chủ (cho task 300 tin)
spam_control = {"is_running": False, "stop_flag": False, "count": 0}

# Khởi tạo client dùng chung
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

async def run_spam_task(base_cmd: str):
    """Tiến trình gửi 300 tin nhắn liên tục tới @deptraikhongsoai_bot"""
    global spam_control
    if spam_control["is_running"]: return
    
    spam_control["is_running"], spam_control["stop_flag"], spam_control["count"] = True, False, 0
    
    try:
        if not client.is_connected(): await client.connect()
        while spam_control["count"] < 300:
            if spam_control["stop_flag"]: break
            
            message = f"{base_cmd} #{spam_control['count']+1} - {time.strftime('%H:%M:%S')}"
            await client.send_message(TARGET_2, message)
            
            spam_control["count"] += 1
            await asyncio.sleep(random.uniform(1.2, 3.5))
    except Exception as e:
        logger.error(f"Spam Error: {str(e)}")
    finally:
        spam_control["is_running"] = False

# --- Endpoints ---

@app.get("/health")
async def health():
    """Ping giữ server sống, KHÔNG gửi tin nhắn"""
    return {"status": "alive"}

@app.get("/diemdanhapple")
async def diemdanh():
    """Gửi 1 tin duy nhất tới @Yuicsa_bot"""
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_1, "/diemdanhapple")
    return {"status": "Sent to Yuicsa_bot"}

@app.get("/work")
async def work():
    """Gửi 1 tin duy nhất tới @deptraikhongsoai_bot"""
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_2, "/work")
    return {"status": "Sent /work to deptraikhongsoai_bot"}

@app.get("/daily")
async def daily():
    """Gửi 1 tin duy nhất tới @deptraikhongsoai_bot"""
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_2, "/daily")
    return {"status": "Sent /daily to deptraikhongsoai_bot"}

@app.get("/stop")
async def stop():
    """Dừng task 300 tin ngầm"""
    spam_control["stop_flag"] = True
    return {"status": "Stopping..."}

@app.get("/{command}")
async def start_spam(command: str):
    """Mọi lệnh khác sẽ gửi 300 tin tới @deptraikhongsoai_bot"""
    if command in ["favicon.ico", "health", "diemdanhapple", "work", "daily", "stop"]:
        return
    full_cmd = f"/{command.replace('-', ' ')}"
    asyncio.create_task(run_spam_task(full_cmd))
    return {"status": "Spam 300 Started", "target": TARGET_2, "cmd": full_cmd}

@app.on_event("startup")
async def startup():
    await client.connect()
