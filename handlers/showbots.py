from aiogram import types
from db.database import get_all_bots

async def show_bots(message: types.Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.reply("У вас нет прав на выполнение этой команды.")
        return

    bots = get_all_bots()
    if not bots:
        await message.reply("Нет клонированных ботов.")
        return

    table = "Имя бота | Telegram ID администратора\n"
    table += "-------------------------------------\n"
    for bot in bots:
        bot_name = bot[3]
        admin_id = bot[2]
        table += f"<code>{bot_name}</code> | <code>{admin_id}</code>\n"

    await message.reply(f"Список клонированных ботов:\n\n{table}", parse_mode=types.ParseMode.HTML)