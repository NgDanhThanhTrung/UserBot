import os
import asyncio
import logging
import random
import re
from fastapi import FastAPI
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION_STR = os.environ.get("SESSION_STR", "")
MONITOR_BOT = os.environ.get("MONITOR_BOT")

spam_control = {"is_running": False, "stop_flag": False}
client = TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH)

@client.on(events.NewMessage(incoming=True))
async def code_handler(event):
    target_bot = "deptraikhongsoai_bot"
    sender = await event.get_sender()
    if hasattr(sender, 'username') and sender.username == MONITOR_BOT:
        text = event.raw_text
        if "Code:" in text:
            match = re.search(r"Code:\s*([^\s\n]+)", text)
            if match:
                gift_code = match.group(1)
                await client.send_message(target_bot, f"/nhapxu {gift_code}")
                logger.info(f"Auto-input code: {gift_code}")

async def auto_scheduler():
    counter = 0
    target_bot = "deptraikhongsoai_bot"
    while True:
        try:
            if not client.is_connected():
                await client.connect()
            await client.send_message(target_bot, "/nhanxu")
            logger.info(f"Auto-sent /nhanxu to @{target_bot}")
            if counter % 3 == 0:
                await asyncio.sleep(random.uniform(10, 12))
                await client.send_message(target_bot, "/work")
                logger.info(f"Auto-sent /work to @{target_bot}")
            if counter % 6 == 0:
                await asyncio.sleep(random.uniform(10, 12))
                await client.send_message(target_bot, "/dao")
                logger.info(f"Auto-sent /dao to @{target_bot}")
            if counter % 72 == 0:
                await asyncio.sleep(random.uniform(10, 12))
                await client.send_message(target_bot, "/daily")
                logger.info(f"Auto-sent /daily to @{target_bot}")
            counter = (counter + 1) % 72
            await asyncio.sleep(600 + random.uniform(5, 10))
        except Exception as e:
            logger.error(f"Auto-scheduler error: {e}")
            await asyncio.sleep(60)

async def run_universal_spam(target: str, base_cmd: str, max_messages: int):
    global spam_control
    if spam_control["is_running"]: return
    spam_control["is_running"], spam_control["stop_flag"] = True, False
    try:
        if not client.is_connected(): await client.connect()
        for i in range(max_messages):
            if spam_control["stop_flag"]: break
            msg_content = f"{base_cmd} #{i + 1}"
            await client.send_message(target, msg_content)
            logger.info(f"Sent to {target}: {msg_content}")
            if i < max_messages - 1:
                wait = random.uniform(6.0, 8.0) if target.lower() == "deptraikhongsoai_bot" else random.uniform(1.5, 3.5)
                await asyncio.sleep(wait)
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
    return {"target": bot_username, "cmd": full_cmd, "count": count}

@app.on_event("startup")
async def startup():
    if API_ID and API_HASH and SESSION_STR:
        await client.connect()
        asyncio.create_task(auto_scheduler())
