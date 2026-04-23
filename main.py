import os
import asyncio
import logging
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

async def run_universal_spam(target: str, content: str, max_messages: int):
    global spam_control
    if spam_control["is_running"]: return
    
    spam_control["is_running"], spam_control["stop_flag"] = True, False
    
    try:
        if not client.is_connected(): await client.connect()
        for i in range(max_messages):
            if spam_control["stop_flag"]: break
            await client.send_message(target, content)
            logger.info(f"Sent to {target}: {content}")
            
            if i < max_messages - 1:
                await asyncio.sleep(0.1) 
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

@app.get("/cmd/{bot_username}/{command}/{count}")
async def trigger_command(bot_username: str, command: str, count: int):
    full_cmd = f"/{command.replace('-', ' ')}"
    asyncio.create_task(run_universal_spam(bot_username, full_cmd, count))
    return {"mode": "command", "target": bot_username, "content": full_cmd, "count": count}

@app.get("/txt/{bot_username}/{text}/{count}")
async def trigger_text(bot_username: str, text: str, count: int):
    clean_text = text.replace('-', ' ')
    asyncio.create_task(run_universal_spam(bot_username, clean_text, count))
    return {"mode": "text", "target": bot_username, "content": clean_text, "count": count}

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
