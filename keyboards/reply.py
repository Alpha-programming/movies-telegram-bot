from aiogram.utils.keyboard import ReplyKeyboardBuilder

def start_kb():
    kb = ReplyKeyboardBuilder()

    kb.button(text='Movies')
    kb.button(text='Cartoons')
    kb.button(text='Dramas')
    kb.button(text='Anime')
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)