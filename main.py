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

app = FastAPI(title="Userbot Secure System")

# --- Lấy thông tin từ Biến môi trường (Environment Variables) ---
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")

# Mục tiêu cố định
TARGET_YUICSA = "Yuicsa_bot"            
TARGET_DEPTRAI = "deptraikhongsoai_bot"   

# Trạng thái điều khiển
spam_control = {"is_running": False, "stop_flag": False, "current_count": 0}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

async def run_custom_spam(base_cmd: str, max_messages: int):
    global spam_control
    if spam_control["is_running"]: return
    spam_control["is_running"], spam_control["stop_flag"], spam_control["current_count"] = True, False, 0
    try:
        if not client.is_connected(): await client.connect()
        while spam_control["current_count"] < max_messages:
            if spam_control["stop_flag"]: break
            await client.send_message(TARGET_DEPTRAI, f"{base_cmd} #{spam_control['current_count']+1}")
            spam_control["current_count"] += 1
            await asyncio.sleep(random.uniform(1.5, 3.5))
    finally:
        spam_control["is_running"] = False

async def run_locket_task(base_cmd: str):
    global spam_control
    if spam_control["is_running"]: return
    spam_control["is_running"], spam_control["stop_flag"] = True, False
    end_time = time.time() + 300
    try:
        if not client.is_connected(): await client.connect()
        while time.time() < end_time:
            if spam_control["stop_flag"]: break
            await client.send_message(TARGET_DEPTRAI, base_cmd)
            await asyncio.sleep(random.uniform(2.5, 4.5))
    finally:
        spam_control["is_running"] = False

# --- API Endpoints ---

@app.get("/health")
async def health():
    return {"status": "alive"}

@app.get("/diemdanhapple")
async def diemdanh():
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_YUICSA, "/diemdanhapple")
    return {"status": "Sent to Yuicsa_bot"}

@app.get("/work")
async def work():
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_DEPTRAI, "/work")
    return {"status": "Sent to Bot 2"}

@app.get("/daily")
async def daily():
    if not client.is_connected(): await client.connect()
    await client.send_message(TARGET_DEPTRAI, "/daily")
    return {"status": "Sent to Bot 2"}

@app.get("/locket-{text}")
async def locket_trigger(text: str):
    full_cmd = f"/locket {text}"
    asyncio.create_task(run_locket_task(full_cmd))
    return {"status": "Locket Started (5 min)"}

@app.get("/stop")
async def stop():
    spam_control["stop_flag"] = True
    return {"status": "Stopped"}

@app.get("/{command}/{count}")
async def dynamic_spam(command: str, count: int):
    if command in ["favicon.ico", "health", "diemdanhapple", "work", "daily", "stop"]: return
    full_cmd = f"/{command.replace('-', ' ')}"
    asyncio.create_task(run_custom_spam(full_cmd, count))
    return {"status": "Started", "cmd": full_cmd, "count": count}

@app.on_event("startup")
async def startup():
    if API_ID == 0 or not API_HASH or not SESSION_STR:
        logger.error("THIẾU BIẾN MÔI TRƯỜNG! Vui lòng kiểm tra API_ID, API_HASH, SESSION_STR")
        return
    await client.connect()
