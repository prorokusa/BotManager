import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.database import get_bot_location

class EditConfig(StatesGroup):
    waiting_for_config = State()

async def edit_config(message: types.Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    bot_location = get_bot_location()
    config_path = os.path.join(bot_location, 'config.py')

    if not os.path.exists(config_path):
        await message.reply("Файл конфигурации не найден.")
        return

    with open(config_path, 'r') as config_file:
        config_content = config_file.read()

    await message.reply(f"Текущий конфиг:\n\n{config_content}\n\nОтправьте новый конфиг:")
    await EditConfig.waiting_for_config.set()

async def process_new_config(message: types.Message, state: FSMContext):
    new_config_content = message.text
    bot_location = get_bot_location()
    config_path = os.path.join(bot_location, 'config.py')

    with open(config_path, 'w') as config_file:
        config_file.write(new_config_content)

    await message.reply("Конфиг успешно обновлен.")
    await state.finish()