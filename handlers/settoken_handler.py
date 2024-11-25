from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.database import get_bot_info_by_name
from handlers.showbots import show_bots
from config import ADMIN_ID
import os

class SetToken(StatesGroup):
    waiting_for_bot_name = State()

async def settoken(message: types.Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    await show_bots(message)
    await message.reply("Введите имя бота, для которого нужно установить токен и админ ID.")
    await SetToken.waiting_for_bot_name.set()

async def process_bot_name(message: types.Message, state: FSMContext):
    bot_name = message.text
    bot_info = get_bot_info_by_name(bot_name)

    if bot_info and bot_info['env_path']:
        try:
            os.makedirs(os.path.dirname(bot_info['env_path']), exist_ok=True)
            with open(bot_info['env_path'], 'w') as env_file:
                env_file.write(f"BOT_TOKEN={bot_info['token']}\n")
                env_file.write(f"ADMIN_ID={bot_info['admin_id']}\n")
            await message.reply(f"Токен и админ ID для бота {bot_name} успешно установлены.")
        except Exception as e:
            await message.reply(f"Ошибка при установке токена: {str(e)}")
    else:
        await message.reply("Бот с таким именем не найден или путь к .env файлу не указан.")

    await state.finish()