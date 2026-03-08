import os
import asyncio
import logging
import random
from fastapi import FastAPI
from telethon import TelegramClient
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")

spam_control = {"is_running": False, "stop_flag": False}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

async def run_universal_spam(target: str, base_cmd: str, max_messages: int):
    global spam_control
    if spam_control["is_running"]: return
    
    is_special = target.lower() == "@deptraikhongsoai_bot"
    
    if is_special:
        final_count = 5
        wait_time = 10
    else:
        final_count = max_messages
        wait_time = None

    spam_control["is_running"], spam_control["stop_flag"] = True, False
    
    try:
        if not client.is_connected(): await client.connect()
        for i in range(final_count):
            if spam_control["stop_flag"]: break
            
            msg_content = f"{base_cmd} #{i + 1}"
            await client.send_message(target, msg_content)
            logger.info(f"Sent to {target}: {msg_content}")
            
            if i < final_count - 1:
                sleep_duration = wait_time if is_special else random.uniform(1.5, 3.5)
                await asyncio.sleep(sleep_duration)
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        spam_control["is_running"] = False

@app.get("/health")
async def health():
    return {"status": "alive"}

@app.get("/stop")
async def stop():
    spam_control["stop_flag"] = True
    return {"status": "stopped"}

@app.get("/{bot_username}/{command}/{count}")
async def dynamic_trigger(bot_username: str, command: str, count: int):
    full_cmd = f"/{command.replace('-', ' ')}"
    asyncio.create_task(run_universal_spam(bot_username, full_cmd, count))
    return {"target": bot_username, "cmd": full_cmd, "count": 5 if bot_username.lower() == "@deptraikhongsoai_bot" else count}

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
