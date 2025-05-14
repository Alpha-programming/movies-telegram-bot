from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

import math

#For Admins
def username():
    kb = InlineKeyboardBuilder()
    kb.button(text='Username',callback_data='username')
    return kb.as_markup()

def main_admin():
    kb = InlineKeyboardBuilder()
    kb.button(text='Add Admin',callback_data='add_admin')
    kb.button(text='Delete Admin', callback_data='delete_admin')
    kb.button(text='Add files', callback_data='add')
    kb.button(text='Delete files', callback_data='del')
    kb.adjust(2)

    return kb.as_markup()

def delete_button(id):
    kb = InlineKeyboardBuilder()
    kb.button(text='Delete Admin',callback_data=f'delete:{id}')

    return kb.as_markup()

def admin_panel():
    kb = InlineKeyboardBuilder()
    kb.button(text='Add file',callback_data='add')
    kb.button(text='Delete files', callback_data='del')

    return kb.as_markup()

def add_files():
    kb = InlineKeyboardBuilder()
    kb.button(text='Movies', callback_data='category:movies')
    kb.button(text='Cartoons', callback_data='category:cartoons')
    kb.button(text='Dramas', callback_data='category:dramas')
    kb.button(text='Anime', callback_data='category:anime')

    return kb.as_markup()

def delete_files():
    kb = InlineKeyboardBuilder()
    kb.button(text='Movies', callback_data='file:movies')
    kb.button(text='Cartoons', callback_data='file:cartoons')
    kb.button(text='Dramas', callback_data='file:dramas')
    kb.button(text='Anime', callback_data='file:anime')

    return kb.as_markup()

def delete_data(id):
    kb = InlineKeyboardBuilder()
    kb.button(text='Delete',callback_data=f'data_delete:{id}')

    return kb.as_markup()

# For Users
def search_button(category):
    kb = InlineKeyboardBuilder()
    kb.button(text='Search By Id', callback_data=f'id_search:{category}')
    kb.button(text='Search By Title', callback_data=f'title_search:{category}')
    kb.button(text='Give all', callback_data=f'all_search:{category}')
    kb.button(text='Search By Genre', callback_data=f'genre_search:{category}')

    kb.adjust(2)
    return kb.as_markup()

def more_button(category, count, total):
    if count >= total:
        return None

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Load More", callback_data=f"more:{category}:{count}")]
        ]
    )
    return keyboard

def more_button_title(category, count, total):
    if count >= total:
        return None

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Load More", callback_data=f"next:{category}:{count}")]
        ]
    )
    return keyboard

def more_button_genre(category, count, total):
    if count >= total:
        return None

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Load More", callback_data=f"extra:{category}:{count}")]
        ]
    )
    return keyboard