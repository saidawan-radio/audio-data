from config import conf
from AudioDetail import AudioDetail
from telethon import TelegramClient
from telethon.tl.types import Message

from datetime import datetime
import json
import os

def create_and_fill_if_empty(file_path:str, default_data:dict):
    if os.path.dirname(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=2)
        print(f"Created/updated {file_path} with data")
        return True
    else:
        print(f"{file_path} already has content")
        return False
            
def load_json(file) -> dict:
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        return data
    
def dump_json(file, data:dict):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    
def audio_detail_update(audio:AudioDetail, data:dict):
    stored_detail_id = data["map_msg_id"][audio.msg_id]
    stored_detail = data["audio_info"][stored_detail_id]
    if load_datetime(audio.edit_date, conf.DATE_FORMAT) > load_datetime(stored_detail["edit_date"], conf.DATE_FORMAT):
        data["audio_info"][stored_detail_id] = audio.to_dict()
        
def load_datetime(strdate, strformat):
    return datetime.strptime(strdate, strformat)

def audio_detail_append(audio:AudioDetail, data:dict):
    if audio.msg_id in data["map_msg_id"]:
        audio.id = data["map_msg_id"][audio.msg_id]
        audio_detail_update(audio, data)
    else:
        data["general_info"]["last_internal_id"] += 1
        audio.id = data["general_info"]["last_internal_id"]
        data["audio_info"][audio.id] = audio.to_dict()
        data["map_msg_id"][audio.msg_id] = audio.id

async def fetch_by_msg_id(client:TelegramClient, channel, msg_id) -> Message:
    msg = await client.get_messages(channel, ids=int(msg_id))
    return msg

async def fetch_by_internal_id(client:TelegramClient, channel, data, internal_id) -> Message:
    msg_id = data["audio_info"][str(internal_id)]["msg_id"]
    return await fetch_by_msg_id(client, channel, int(msg_id))
        
async def audio_detail_fetcher(client:TelegramClient, channel, min_id:int, data_limit:int, duration_limit:int, data:dict):
    async for msg in client.iter_messages(channel, min_id=min_id, reverse=True, limit=data_limit):
        if not msg.audio:
            continue
        audio = AudioDetail(msg)
        if audio.duration <= duration_limit:
            audio_detail_append(audio, data)
    return data


async def fetch_and_write_detail(client:TelegramClient, channel, min_id:int, data_limit:int, duration_limit:int, data:dict, file_path:str):
    data = await audio_detail_fetcher(client, channel, min_id, data_limit, duration_limit, data)
    dump_json(file_path, data)
    