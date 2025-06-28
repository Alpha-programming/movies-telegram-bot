from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import Router, F
from misc.state import Username, AddUsername, AddMediaState, IdMediaSearchState
from keyboards.inline import main_admin, delete_button, admin_panel, add_files, delete_data, delete_files, more_button, more_button_title, more_button_genre, username
from database.database import admin_repo, media_repo

router = Router()

# For Admins
@router.callback_query(F.data.startswith('username'))
async def request_username(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='👤 Please write the special username.')
    await state.set_state(Username.username)

@router.message(Username.username)
async def username_panel(message: Message, state: FSMContext):
    username = message.text
    chat_id = message.from_user.id
    admin_dict = {admin[2]: admin[3] for admin in admin_repo.get_admin_list()}
    admin_id_username_dict = {admin[1]: admin[2] for admin in admin_repo.get_admin_list()}

    if chat_id == 425148431 and username == 'alpha':
        await message.answer(text=f'✅ Welcome {username} admin. Please choose an action below.', reply_markup=main_admin())
    elif admin_id_username_dict.get(chat_id) == username and admin_dict[username] != 'main':
        await message.answer(
            text=f"✅ Welcome {username} admin. Please choose an action below.\n\nPress '📤 Add' to upload files or '🗑️ Delete' to remove files.",
            reply_markup=admin_panel()
        )
    else:
        await message.answer(text='❌ Incorrect username or Telegram ID. Please try again.')

@router.callback_query(F.data.startswith('add_admin'))
async def add_admin(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='➕ Write the username, telegram ID, and role separated by colons (e.g., user:123456:admin)')
    await state.set_state(AddUsername.user)

@router.message(AddUsername.user)
async def receive_dat_admin(message: Message, state: FSMContext):
    username, chat_id, role = message.text.split(':')

    if admin_repo.add_admins(chat_id, username, role):
        await message.answer(text=f'✅ Admin {username} added successfully!', reply_markup=main_admin())
    else:
        await message.answer(text='❌ Admin with this Telegram ID already exists.', reply_markup=main_admin())

@router.callback_query(F.data.startswith('delete_admin'))
async def delete_admin(call: CallbackQuery):
    admin_list = admin_repo.get_admin_list()
    for admin in admin_list:
        text = f'🆔 ID: {admin[0]}\n👤 Telegram ID: {admin[1]}\n🔤 Username: {admin[2]}\n🔰 Role: {admin[3]}'
        if admin[3] == 'main':
            await call.message.answer(text=text)
        else:
            await call.message.answer(text=text, reply_markup=delete_button(admin[0]))

@router.callback_query(F.data.startswith('delete'))
async def admin_deleted(call: CallbackQuery):
    _, admin_id = call.data.split(':')
    if admin_repo.delete_admin(admin_id):
        await call.message.answer(text=f'✅ Admin with ID {admin_id} deleted.', reply_markup=main_admin())

@router.callback_query(F.data.startswith('add'))
async def add_files_category(call: CallbackQuery):
    await call.message.edit_text(
        text="🎯 Choose a category to **add files**:\n\n🎬 Movies\n📺 Cartoons\n🎭 Dramas\n🌸 Anime",
        reply_markup=add_files()
    )

@router.callback_query(F.data.startswith('category'))
async def add_file(call: CallbackQuery, state: FSMContext):
    _, category = call.data.split(':')
    await state.update_data(category=category)
    await call.message.answer(text="✏️ Send the **title** of the file.")
    await state.set_state(AddMediaState.title)

@router.message(AddMediaState.title)
async def receive_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("🎭 Now send the **genre** of the file.")
    await state.set_state(AddMediaState.genre)

@router.message(AddMediaState.genre)
async def receive_genre(message: Message, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("📤 Now send the **video file**.")
    await state.set_state(AddMediaState.file)

@router.message(AddMediaState.file, F.video | F.document)
async def receive_file(message: Message, state: FSMContext):
    chat_id = message.from_user.id
    file_id = message.video.file_id if message.video else message.document.file_id if message.document and message.document.mime_type.startswith('video/') else None

    if not file_id:
        await message.answer("❌ Invalid file type. Please upload a video file.")
        return

    data = await state.get_data()
    title, category, genre = data["title"], data["category"], data['genre']

    if media_repo.add_media(title, file_id, category, genre):
        markup = main_admin() if admin_repo.check_admin_role(chat_id) == 'main' else admin_panel()
        await message.answer(f"✅ {category.capitalize()} '{title}' added successfully!", reply_markup=markup)
    else:
        markup = main_admin() if admin_repo.check_admin_role(chat_id) == 'main' else admin_panel()
        await message.answer(f"❌ '{title}' already exists.", reply_markup=markup)

    await state.clear()

@router.callback_query(F.data.startswith('del'))
async def delete_files_categories(call: CallbackQuery):
    await call.message.edit_text(
        text="🗑️ Choose a category to **delete files**:\n\n🎬 Movies\n📺 Cartoons\n🎭 Dramas\n🌸 Anime",
        reply_markup=delete_files()
    )

@router.callback_query(F.data.startswith('file'))
async def delete_file(call: CallbackQuery, state: FSMContext):
    _, category = call.data.split(':')
    chat_id = call.from_user.id
    files = media_repo.get_files_by_category(category)

    if not files:
        markup = main_admin() if admin_repo.check_admin_role(chat_id) == 'main' else admin_panel()
        await call.message.answer(f"❌ No files found in {category}.", reply_markup=markup)
        return

    for file in files:
        id, file_id, title = file[0], file[1], file[2]
        await call.message.answer(text=f"🎬 {title}", reply_markup=delete_data(id))

@router.callback_query(F.data.startswith('data_delete'))
async def confirm_delete(call: CallbackQuery, state: FSMContext):
    _, id = call.data.split(':')
    chat_id = call.from_user.id
    if media_repo.delete_file(id):
        markup = main_admin() if admin_repo.check_admin_role(chat_id) == 'main' else admin_panel()
        await call.message.answer("✅ File deleted successfully.", reply_markup=markup)
    else:
        markup = main_admin() if admin_repo.check_admin_role(chat_id) == 'main' else admin_panel()
        await call.message.answer("❌ Error! File could not be deleted.", reply_markup=markup)

# User Handlers

@router.callback_query(F.data.startswith('id_search'))
async def id_search(call: CallbackQuery, state: FSMContext):
    _, category = call.data.split(':')
    await state.update_data(category=category)
    await call.message.answer(text=f'🔍 Write the **ID** of {category}')
    await state.set_state(IdMediaSearchState.id_search)

@router.message(IdMediaSearchState.id_search)
async def id_search_receive(message: Message, state: FSMContext):
    data_state = await state.get_data()
    category = data_state['category']
    search_id = message.text
    data = media_repo.search_media_id(search_id, category)
    if data:
        file_id, title, genre = data
        await message.answer_video(file_id, caption=f"🎬 {title}\n🎭 Genre: {genre}")
    else:
        await message.answer(f"❌ No matching {category} found.")

@router.callback_query(F.data.startswith('title_search'))
async def title_search(call: CallbackQuery, state: FSMContext):
    _, category = call.data.split(':')
    await state.update_data(category=category)
    await call.message.answer(text=f'🔎 Write the **title** of {category}')
    await state.set_state(IdMediaSearchState.title_search)

@router.message(IdMediaSearchState.title_search)
async def title_search_receive(message: Message, state: FSMContext):
    data_state = await state.get_data()
    category = data_state['category']
    search_title = message.text
    data_list = media_repo.search_media_title(search_title, category)
    await state.update_data(search_title=search_title)
    total = len(data_list)

    if data_list:
        for data in data_list[:10]:
            file_id, title, genre = data
            await message.answer_video(file_id, caption=f"🎬 {title}\n🎭 Genre: {genre}")
        if total > 10:
            await message.answer(text='🔁 More results available:', reply_markup=more_button_title(category, 10, total))
    else:
        await message.answer(f"❌ No matching {category} found.")

@router.callback_query(F.data.startswith('next'))
async def next_title_search(call: CallbackQuery, state: FSMContext):
    dat_state = await state.get_data()
    search_title = dat_state['search_title']
    _, category, count = call.data.split(':')
    count = int(count)
    finish_count = count + 10
    media_list = media_repo.search_media_title(search_title, category)
    total = len(media_list)

    if count >= total:
        await call.message.answer(f"✅ No more files found in {category}.")
        return

    for data in media_list[count:finish_count]:
        file_id, title, genre = data
        await call.message.answer_video(file_id, caption=f"🎬 {title}\n🎭 Genre: {genre}")
    if total > finish_count:
        await call.message.answer(text='🔁 More results available:', reply_markup=more_button_title(category, finish_count, total))

@router.callback_query(F.data.startswith('all_search'))
async def all_search(call: CallbackQuery, state: FSMContext):
    _, category = call.data.split(':')
    media_list = media_repo.get_files_by_category(category)
    total = len(media_list)

    if not media_list:
        await call.message.answer(f"❌ No media files found in the {category} category.")
        return

    response_text = f"🎬 **Available {category.capitalize()}**\n\n"
    for data in media_list[:10]:
        response_text += f"📌 **ID:** `{data[0]}`\n🎥 **Title:** {data[2]}\n🎭 Genre: {data[3]}\n\n"

    await call.message.answer(text=response_text, reply_markup=more_button(category, 10, total))

@router.callback_query(F.data.startswith('more'))
async def more_search(call: CallbackQuery, state: FSMContext):
    _, category, count = call.data.split(':')
    count = int(count)
    finish_count = count + 10
    media_list = media_repo.get_files_by_category(category)
    total = len(media_list)

    if count >= total:
        await call.message.answer(f"✅ No more media files found in the {category} category.")
        return

    response_text = f"🎬 **More {category.capitalize()}**\n\n"
    for data in media_list[count:finish_count]:
        response_text += f"📌 **ID:** `{data[0]}`\n🎥 **Title:** {data[2]}\n\n"

    await call.message.answer(text=response_text, reply_markup=more_button(category, finish_count, total))

@router.callback_query(F.data.startswith('genre_search'))
async def genre_search(call: CallbackQuery, state: FSMContext):
    _, category = call.data.split(':')
    await state.update_data(category=category)
    await call.message.answer(text=f'🔎 Write the **genre** of {category}')
    await state.set_state(IdMediaSearchState.genre_search)

@router.message(IdMediaSearchState.genre_search)
async def genre_search_receive(message: Message, state: FSMContext):
    data_state = await state.get_data()
    category = data_state['category']
    genre = message.text
    data_list = media_repo.search_media_genre(genre, category)
    await state.update_data(genre=genre)
    total = len(data_list)

    if data_list:
        for data in data_list[:10]:
            file_id, title, genre = data
            await message.answer_video(file_id, caption=f"🎬 {title}\n🎭 Genre: {genre}")
        if total > 10:
            await message.answer(text='🔁 More results available:', reply_markup=more_button_genre(category, 10, total))
    else:
        await message.answer(f"❌ No matching {category} found.")

@router.callback_query(F.data.startswith('extra'))
async def extra_genre_search(call: CallbackQuery, state: FSMContext):
    data_state = await state.get_data()
    genre = data_state['genre']
    _, category, count = call.data.split(':')
    count = int(count)
    finish_count = count + 10
    media_list = media_repo.search_media_genre(genre, category)
    total = len(media_list)

    if count >= total:
        await call.message.answer(f"✅ No more media files found in the {category} category.")
        return

    for data in media_list[count:finish_count]:
        file_id, title, genre = data
        await call.message.answer_video(file_id, caption=f"🎬 {title}\n🎭 Genre: {genre}")
    if total > finish_count:
        await call.message.answer(text='🔁 More results available:', reply_markup=more_button_genre(category, finish_count, total))
