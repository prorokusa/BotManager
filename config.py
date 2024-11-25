import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

BOT_TOKEN = os.getenv('BOT_MANAGER_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_MANAGER_TOKEN не найден в переменных окружения")

ADMIN_ID = os.getenv('ADMIN_ID')
if not ADMIN_ID:
    raise ValueError("ADMIN_ID не найден в переменных окружения")
try:
    ADMIN_ID = int(ADMIN_ID)
except ValueError:
    raise ValueError("ADMIN_ID должен быть числом")