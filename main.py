import os
import asyncio
import logging
import time
import random
from fastapi import FastAPI, Path
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="Userbot Custom Count - Render")

# --- Cấu hình Mục tiêu ---
TARGET_1 = "Yuicsa_bot"            
TARGET_2 = "deptraikhongsoai_bot"   

API_ID = 39516756
API_HASH = "02b3f7dfef549f670c3eb938912754c8"
SESSION_STR = os.environ.get("SESSION_STR", "")

# Trạng thái điều khiển
spam_control = {"is_running": False, "stop_flag": False, "current_count": 0}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

async def run_custom_spam(base_cmd: str, max_messages: int):
    """Gửi tin nhắn theo số lần yêu cầu"""
    global spam_control
    if spam_control["is_running"]: return
    
    spam_control["is_running"], spam_control["stop_flag"], spam_control["current_count"] = True, False, 0
    
    try:
        if not client.is_connected(): await client.connect()
        logger.info(f"Bắt đầu gửi {max_messages} tin: {base_cmd}")
        
        while spam_control["current_count"] < max_messages:
            if spam_control["stop_flag"]: break
            
            # Nội dung tin nhắn
            msg = f"{base_cmd} #{spam_control['current_count']+1}"
            await client.send_message(TARGET_2, msg)
            
            spam_control["current_count"] += 1
            await asyncio.sleep(random.uniform(1.2, 3.5))
            
    except Exception as e:
        logger.error(f"Lỗi: {str(e)}")
    finally:
        spam_control["is_running"] = False

async def run_locket_task(base_cmd: str):
    """Gửi lệnh locket liên tục trong 5 phút"""
    global spam_control
    if spam_control["is_running"]: return
    spam_control["is_running"], spam_control["stop_flag"] = True, False
    end_time = time.time() + 300
    try:
        if not client.is_connected(): await client.connect()
        while time.time() < end_time:
            if spam_control["stop_flag"]: break
            await client.send_message(TARGET_2, base_cmd)
            await asyncio.sleep(random.uniform(2.0, 4.0))
    finally:
        spam_control["is_running"] = False

# --- Endpoints ---

@app.get("/health")
async def health():
    return {"status": "alive"}

@app.get("/diemdanhapple")
async def diemdanh():
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_1, "/diemdanhapple")
    return {"status": "Sent to Yuicsa_bot"}

@app.get("/work")
async def work():
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_2, "/work")
    return {"status": "Sent /work to Bot 2"}

@app.get("/daily")
async def daily():
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_2, "/daily")
    return {"status": "Sent /daily to Bot 2"}

@app.get("/locket-{text}")
async def locket_trigger(text: str):
    full_cmd = f"/locket {text}"
    asyncio.create_task(run_locket_task(full_cmd))
    return {"status": "Locket Started (5 min)", "cmd": full_cmd}

@app.get("/stop")
async def stop():
    spam_control["stop_flag"] = True
    return {"status": "Stopping..."}

# ĐÂY LÀ PHẦN THAY ĐỔI CHÍNH: /lenh-abc/10
@app.get("/{command}/{count}")
async def start_custom_spam(command: str, count: int):
    """Truy cập /abc-xyz/50 để gửi lệnh /abc xyz 50 lần"""
    # Xử lý lệnh
    full_cmd = f"/{command.replace('-', ' ')}"
    
    # Chạy task với số lần tùy chỉnh
    asyncio.create_task(run_custom_spam(full_cmd, count))
    
    return {
        "status": "Started",
        "command": full_cmd,
        "target_count": count,
        "target_user": TARGET_2
    }

@app.on_event("startup")
async def startup():
    await client.connect()
