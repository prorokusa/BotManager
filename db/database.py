import sqlite3

def init_db():
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS botforclone (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            token TEXT NOT NULL,
            admin_id TEXT NOT NULL,
            bot_name TEXT NOT NULL,
            config_path TEXT,
            env_path TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_bot_info(bot_name, token, admin_id, bot_path):
    try:
        conn = sqlite3.connect('botmanager.db')
        cursor = conn.cursor()
        
        # Создаем таблицу, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                token TEXT NOT NULL,
                admin_id INTEGER NOT NULL,
                path TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Добавляем информацию о боте
        cursor.execute('''
            INSERT INTO bots (name, token, admin_id, path)
            VALUES (?, ?, ?, ?)
        ''', (bot_name, token, admin_id, bot_path))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка при сохранении информации о боте: {e}")
        return False

def save_bot_location(location):
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE botforclone SET location = ? WHERE id = (SELECT MAX(id) FROM botforclone)', (location,))
    conn.commit()
    conn.close()

def save_config_path(config_path):
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE botforclone SET config_path = ? WHERE id = (SELECT MAX(id) FROM botforclone)', (config_path,))
    conn.commit()
    conn.close()

def save_env_path(env_path):
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE botforclone SET env_path = ? WHERE id = (SELECT MAX(id) FROM botforclone)', (env_path,))
    conn.commit()
    conn.close()

def get_bot_location():
    try:
        conn = sqlite3.connect('botmanager.db')
        cursor = conn.cursor()
        cursor.execute('SELECT location FROM botforclone ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"Ошибка при получении локации бота: {e}")
        return None

def get_all_bots():
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM botforclone')
    bots = cursor.fetchall()
    conn.close()
    return bots

def get_bot_info_by_name(bot_name):
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token, admin_id, env_path FROM botforclone WHERE bot_name = ?', (bot_name,))
    bot_info = cursor.fetchone()
    conn.close()
    if bot_info:
        return {
            'token': bot_info[0],
            'admin_id': bot_info[1],
            'env_path': bot_info[2]
        }
    return None