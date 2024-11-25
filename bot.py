import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import BOT_TOKEN
from handlers import start, clone, edit_config, showbots
from db.database import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

if __name__ == '__main__':
    init_db()
    dp.register_message_handler(start.start, commands=['start'])
    dp.register_message_handler(clone.clone_bot, commands=['clone'])
    dp.register_message_handler(edit_config.edit_config, commands=['edit_config'])
    dp.register_message_handler(edit_config.process_new_config, state=edit_config.EditConfig.waiting_for_config)
    dp.register_message_handler(showbots.show_bots, commands=['showbots'])
    executor.start_polling(dp, skip_updates=True)