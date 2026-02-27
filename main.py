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

app = FastAPI()

# Cấu hình cứng
API_ID = 39516756
API_HASH = "02b3f7dfef549f670c3eb938912754c8"
TARGET_DIEMDANH = "Yuicsa_bot"
TARGET_SPAM = "deptraikhongsoai_bot"
SESSION_STR = os.environ.get("SESSION_STR", "")

# Quản lý trạng thái
spam_control = {"is_running": False, "stop_flag": False, "count": 0}

# Khởi tạo client
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

async def run_spam_task(base_cmd: str):
    global spam_control
    if spam_control["is_running"]:
        return
    
    spam_control["is_running"] = True
    spam_control["stop_flag"] = False
    spam_control["count"] = 0
    
    try:
        if not client.is_connected():
            await client.connect()
            
        while spam_control["count"] < 300:
            if spam_control["stop_flag"]:
                logger.info("Server: Received stop signal.")
                break
                
            msg = f"{base_cmd} #{spam_control['count']+1} - {time.strftime('%H:%M:%S')}"
            await client.send_message(TARGET_SPAM, msg)
            
            spam_control["count"] += 1
            await asyncio.sleep(random.uniform(1.2, 3.5))
            
    except FloodWaitError as e:
        logger.warning(f"FloodWait: Sleeping for {e.seconds}s")
        await asyncio.sleep(e.seconds + 10)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
    finally:
        spam_control["is_running"] = False

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/diemdanhapple")
async def diemdanh():
    try:
        if not client.is_connected():
            await client.connect()
        await client.send_message(TARGET_DIEMDANH, "/diemdanhapple")
        return {"status": "Success", "target": TARGET_DIEMDANH}
    except Exception as e:
        return {"status": "Error", "detail": str(e)}

@app.get("/stop")
async def stop_server():
    spam_control["stop_flag"] = True
    return {"status": "Stopping..."}

@app.get("/{command}")
async def start_spam(command: str):
    if command in ["favicon.ico", "health", "diemdanhapple", "stop"]:
        return
    full_cmd = f"/{command.replace('-', ' ')}"
    asyncio.create_task(run_spam_task(full_cmd))
    return {"status": "Spam Started", "cmd": full_cmd, "target": TARGET_SPAM}

@app.on_event("startup")
async def startup():
    if not client.is_connected():
        await client.connect()
    logger.info("Bot started successfully.")
