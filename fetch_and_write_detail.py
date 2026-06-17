from FetchDetail import create_and_fill_if_empty,load_json,fetch_and_write_detail
from config import conf
from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio

create_and_fill_if_empty(conf.DATA_FILE_PATH, conf.JSON_DATA_FORM)

# proxy = ("http", "127.0.0.1", 10808)

data = load_json(conf.DATA_FILE_PATH)
SESSION_STR = conf.SESSION_STR
session = StringSession(SESSION_STR)
client = TelegramClient(session, conf.API_ID, conf.API_HASH)


async def main():
    await client.start()
    channel = await client.get_input_entity(conf.CHANNEL_USERNAME)
    await fetch_and_write_detail(client, channel, conf.MIN_MSG_ID, conf.DATA_FETCH_LIMIT, conf.DURATION_LIMIT, data, conf.DATA_FILE_PATH)

asyncio.run(main())

    
