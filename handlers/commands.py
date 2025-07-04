from aiogram import Router,Bot
from aiogram.types import Message
from aiogram.filters.command import CommandStart,Command
from keyboards.reply import start_kb
from keyboards.inline import username, follow_channel_button
from database.database import admin_repo
from .check_sub import is_user_subscribed

router = Router()

@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    if not await is_user_subscribed(bot, message.from_user.id):
        await message.answer(
            "❗️To use this bot, please join our channel first:",
            reply_markup=follow_channel_button()
        )
        return

    admin_repo.add_main_admin(425148431, 'alpha')
    await message.answer('✅ Welcome to the Movies Bot', reply_markup=start_kb())
@router.message(Command(commands='upload'))
async def upload(message: Message):
    await message.answer(text='If you want to upload a movie. Please press button below to pass the authentication.',reply_markup=username())

@router.message(Command(commands='info'))
async def info(message: Message):
    await message.answer(text="This bot helps users to search for and download various types of movies in 'Movies', cartoons in 'Cartoons',soap opera and drama in 'Dramas' and anime in 'Anime' categories.")
