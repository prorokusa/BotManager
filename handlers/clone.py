import os
import shutil
import zipfile
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.database import save_bot_info, save_bot_location

class CloneBot(StatesGroup):
    waiting_for_token = State()
    waiting_for_admin_id = State()
    waiting_for_bot_name = State()
    waiting_for_archive = State()

async def clone_bot(message: types.Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    await message.reply("Отправьте токен нового бота.")
    await CloneBot.waiting_for_token.set()

async def process_token(message: types.Message, state: FSMContext):
    token = message.text
    await state.update_data(token=token)
    await message.reply("Отправьте Telegram ID администратора.")
    await CloneBot.waiting_for_admin_id.set()

async def process_admin_id(message: types.Message, state: FSMContext):
    admin_id = message.text
    await state.update_data(admin_id=admin_id)
    await message.reply("Отправьте имя нового бота.")
    await CloneBot.waiting_for_bot_name.set()

async def process_bot_name(message: types.Message, state: FSMContext):
    bot_name = message.text
    await state.update_data(bot_name=bot_name)
    await message.reply("Отправьте архив с ботом, который нужно клонировать.")
    await CloneBot.waiting_for_archive.set()

async def process_archive(message: types.Message, state: FSMContext):
    archive = message.document
    file_id = archive.file_id
    file_info = await message.bot.get_file(file_id)
    file_path = file_info.file_path

    download_path = f"downloads/{file_id}.zip"
    await message.bot.download_file(file_path, download_path)

    data = await state.get_data()
    bot_name = data.get('bot_name')
    clone_dir = os.path.join("CloneBots", bot_name)

    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)

    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(clone_dir)

    # Перемещаем содержимое архива на один уровень выше, если это необходимо
    for item in os.listdir(clone_dir):
        s = os.path.join(clone_dir, item)
        d = os.path.join(clone_dir, item)
        if os.path.isdir(s):
            shutil.move(s, d)

    token = data.get('token')
    admin_id = data.get('admin_id')

    save_bot_info(token, admin_id, bot_name)
    save_bot_location(clone_dir)

    await message.reply(f"Бот успешно клонирован в директорию {clone_dir}.")
    await state.finish()