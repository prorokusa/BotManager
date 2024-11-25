from aiogram import types

async def start(message: types.Message):
    await message.reply("Привет! Я бот BotManager. Используй /clone для создания клона бота.")