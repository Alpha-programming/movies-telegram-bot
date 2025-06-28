from aiogram import Router,F
from aiogram.types import Message
from keyboards.inline import search_button
router = Router()

@router.message(F.text == '🎬Movies')
async def blackjack(message: Message):
    await message.reply(text='If you want to download a movie.Please choose the action',reply_markup=search_button('movies'))

@router.message(F.text == '📺Cartoons')
async def blackjack(message: Message):
    await message.reply(text='If you want to download a cartoon.Please choose the action',reply_markup=search_button('cartoons'))

@router.message(F.text == '🎭Dramas')
async def blackjack(message: Message):
    await message.reply(text='If you want to download a drama.Please choose the action',reply_markup=search_button('dramas'))

@router.message(F.text == '🌸Anime')
async def blackjack(message: Message):
    await message.reply(text='If you want to download an anime.Please choose the action',reply_markup=search_button('anime'))


@router.message(F.text == "📩 Request")
async def request_movies_handler(message: Message):
    bot_link = "https://t.me/@alphacoding_bot"  # Replace with your bot username

    msg = (
        "🚀 To request or send movies, cartoons, dramas, or anime, please contact via this bot link:\n"
        f"👉 {bot_link}\n\n"
        "💼 If you want to order a new bot or become a partner, contact us:\n\n"

        "**English:**\n"
        "📩 Send your requests or partnership offers anytime.\n\n"

        "**O‘zbekcha:**\n"
        "📩 Filmlar, multfilmlar, dramas yoki anime so‘rovlari va fayllarini yuborish uchun botga murojaat qiling.\n"
        "📩 Yangi bot buyurtma qilish yoki hamkor bo‘lish uchun murojaat qiling.\n\n"

        "**Русский:**\n"
        "📩 Запросы или файлы фильмов, мультфильмов, драм или аниме отправляйте через бота.\n"
        "📩 Закажите нового бота или станьте партнёром, свяжитесь с нами."
    )

    await message.answer(msg)

