import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import BOT_TOKEN
from handlers import start, clone_handler, settoken_handler, edit_config, showbots
from db.database import init_db
from handlers.clone_handler import register_clone_handlers
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())

def main():
    init_db()
    dp.register_message_handler(start.start, commands=['start'])
    register_clone_handlers(dp)
    dp.register_message_handler(settoken_handler.settoken, commands=['settoken'])
    dp.register_message_handler(settoken_handler.process_bot_name, state=settoken_handler.SetToken.waiting_for_bot_name)
    dp.register_message_handler(edit_config.edit_config, commands=['edit_config'])
    dp.register_message_handler(edit_config.process_new_config, state=edit_config.EditConfig.waiting_for_config)
    dp.register_message_handler(showbots.show_bots, commands=['showbots'])
    executor.start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()