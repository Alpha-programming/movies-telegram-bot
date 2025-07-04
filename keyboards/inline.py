from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton

# For Admins
def username():
    kb = InlineKeyboardBuilder()
    kb.button(text='👤 Username', callback_data='username')
    return kb.as_markup()

def main_admin():
    kb = InlineKeyboardBuilder()
    kb.button(text='➕ Add Admin', callback_data='add_admin')
    kb.button(text='🗑️ Delete Admin', callback_data='delete_admin')
    kb.button(text='📤 Add Files', callback_data='add')
    kb.button(text='🗂️ Delete Files', callback_data='del')
    kb.adjust(2)
    return kb.as_markup()

def delete_button(id):
    kb = InlineKeyboardBuilder()
    kb.button(text='🗑️ Delete Admin', callback_data=f'delete:{id}')
    return kb.as_markup()

def admin_panel():
    kb = InlineKeyboardBuilder()
    kb.button(text='📤 Add File', callback_data='add')
    kb.button(text='🗂️ Delete Files', callback_data='del')
    return kb.as_markup()

def add_files():
    kb = InlineKeyboardBuilder()
    kb.button(text='🎬 Movies', callback_data='category:movies')
    kb.button(text='📺 Cartoons', callback_data='category:cartoons')
    kb.button(text='🎭 Dramas', callback_data='category:dramas')
    kb.button(text='🌸 Anime', callback_data='category:anime')
    kb.adjust(2)
    return kb.as_markup()

def delete_files():
    kb = InlineKeyboardBuilder()
    kb.button(text='🗑️ 🎬 Movies', callback_data='file:movies')
    kb.button(text='🗑️ 📺 Cartoons', callback_data='file:cartoons')
    kb.button(text='🗑️ 🎭 Dramas', callback_data='file:dramas')
    kb.button(text='🗑️ 🌸 Anime', callback_data='file:anime')
    kb.adjust(2)
    return kb.as_markup()

def delete_data(id):
    kb = InlineKeyboardBuilder()
    kb.button(text='🗑️ Delete', callback_data=f'data_delete:{id}')
    return kb.as_markup()

# For Users
def search_button(category):
    kb = InlineKeyboardBuilder()
    kb.button(text='🔍 Search by ID', callback_data=f'id_search:{category}')
    kb.button(text='🔎 Search by Title', callback_data=f'title_search:{category}')
    kb.button(text='📚 Give All', callback_data=f'all_search:{category}')
    kb.button(text='🎯 Search by Genre', callback_data=f'genre_search:{category}')
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

def follow_channel_button():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Join Channel", url="https://t.me/@moviesfreewatch7")],
        [InlineKeyboardButton(text="✅ I've Joined", callback_data="check_subscription")]
    ])