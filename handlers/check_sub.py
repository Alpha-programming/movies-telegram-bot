from aiogram import Bot
from aiogram.types import ChatMember
import os
from dotenv import load_dotenv
load_dotenv()

CHANNEL_USERNAME =  os.getenv("CHANNEL_USERNAME")

async def is_user_subscribed(bot: Bot, user_id: int) -> bool:
    try:
        member: ChatMember = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False
