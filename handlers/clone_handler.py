import os
import shutil
import zipfile
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from db.database import save_bot_info, save_bot_location, save_config_path, save_env_path
from config import ADMIN_ID

class CloneBot(StatesGroup):
    waiting_for_token = State()
    waiting_for_admin_id = State()
    waiting_for_bot_name = State()
    waiting_for_archive = State()

async def clone_bot(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return
    
    await message.reply("Начинаем процесс клонирования бота.\nПожалуйста, отправьте токен нового бота.")
    await CloneBot.waiting_for_token.set()

async def process_token(message: types.Message, state: FSMContext):
    try:
        token = message.text
        await state.update_data(token=token)
        await message.reply("Токен успешно сохранен.\nТеперь отправьте Telegram ID администратора.")
        await CloneBot.waiting_for_admin_id.set()
    except Exception as e:
        await message.reply(f"Ошибка при сохранении токена: {e}\nПопробуйте еще раз.")
        await state.finish()

async def process_admin_id(message: types.Message, state: FSMContext):
    try:
        admin_id = int(message.text)
        await state.update_data(admin_id=admin_id)
        await message.reply("ID администратора сохранен.\nТеперь введите имя для нового бота.")
        await CloneBot.waiting_for_bot_name.set()
    except ValueError:
        await message.reply("Ошибка: ID администратора должен быть числом.\nПопробуйте еще раз.")
    except Exception as e:
        await message.reply(f"Ошибка при сохранении ID администратора: {e}\nПопробуйте еще раз.")
        await state.finish()

async def process_bot_name(message: types.Message, state: FSMContext):
    try:
        bot_name = message.text
        await state.update_data(bot_name=bot_name)
        await message.reply(
            "Имя бота сохранено.\n"
            "Теперь отправьте архив с кодом бота (zip или tar.gz).\n"
            "Архив должен содержать все необходимые файлы для работы бота."
        )
        await CloneBot.waiting_for_archive.set()
    except Exception as e:
        await message.reply(f"Ошибка при сохранении имени бота: {e}\nПопробуйте еще раз.")
        await state.finish()

async def process_archive(message: types.Message, state: FSMContext):
    try:
        await message.reply("Начинаю обработку архива...")
        
        # Получаем сохраненные данные
        data = await state.get_data()
        bot_name = data['bot_name']
        token = data['token']
        admin_id = data['admin_id']

        # Создаем директории
        base_dir = "bots"
        clone_dir = os.path.join(base_dir, bot_name)
        os.makedirs(clone_dir, exist_ok=True)
        await message.reply(f"Создана директория для бота: {clone_dir}")

        # Скачиваем архив
        download_path = os.path.join("downloads", message.document.file_name)
        os.makedirs("downloads", exist_ok=True)
        await message.reply("Скачиваю архив...")
        await message.document.download(destination_file=download_path)

        # Распаковываем архив
        await message.reply("Распаковываю архив...")
        if download_path.endswith('.zip'):
            shutil.unpack_archive(download_path, clone_dir, 'zip')
        elif download_path.endswith('.tar.gz'):
            shutil.unpack_archive(download_path, clone_dir, 'gztar')
        else:
            raise ValueError("Неподдерживаемый формат архива. Используйте .zip или .tar.gz")

        # Создаем .env файл
        env_path = os.path.join(clone_dir, '.env')
        with open(env_path, 'w') as env_file:
            env_file.write(f"BOT_TOKEN={token}\n")
            env_file.write(f"ADMIN_ID={admin_id}\n")
        await message.reply("Создан файл конфигурации .env")

        # Записываем информацию в базу данных
        save_bot_info(bot_name, token, admin_id, clone_dir)
        await message.reply("Информация о боте сохранена в базе данных")

        # Удаляем временные файлы
        if os.path.exists(download_path):
            os.remove(download_path)

        await message.reply(
            f"✅ Клонирование бота успешно завершено!\n\n"
            f"📁 Путь к боту: {clone_dir}\n"
            f"🤖 Имя бота: {bot_name}\n"
            f"👤 ID администратора: {admin_id}\n\n"
            f"Теперь вы можете запустить бота из указанной директории."
        )

    except Exception as e:
        await message.reply(f"❌ Ошибка при клонировании бота: {str(e)}")
    finally:
        await state.finish()

def register_clone_handlers(dp):
    dp.register_message_handler(clone_bot, commands=['clone'])
    dp.register_message_handler(process_token, state=CloneBot.waiting_for_token)
    dp.register_message_handler(process_admin_id, state=CloneBot.waiting_for_admin_id)
    dp.register_message_handler(process_bot_name, state=CloneBot.waiting_for_bot_name)
    dp.register_message_handler(process_archive, state=CloneBot.waiting_for_archive, content_types=['document'])