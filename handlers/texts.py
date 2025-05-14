from aiogram import Router,F
from aiogram.types import Message
from keyboards.inline import search_button
router = Router()

@router.message(F.text == 'Movies')
async def blackjack(message: Message):
    await message.reply(text='If you want to download a movie.Please choose the action',reply_markup=search_button('movies'))

@router.message(F.text == 'Cartoons')
async def blackjack(message: Message):
    await message.reply(text='If you want to download a cartoon.Please choose the action',reply_markup=search_button('cartoons'))

@router.message(F.text == 'Dramas')
async def blackjack(message: Message):
    await message.reply(text='If you want to download a drama.Please choose the action',reply_markup=search_button('dramas'))

@router.message(F.text == 'Anime')
async def blackjack(message: Message):
    await message.reply(text='If you want to download an anime.Please choose the action',reply_markup=search_button('anime'))