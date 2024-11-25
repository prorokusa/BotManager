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
            bot_name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_bot_info(token, admin_id, bot_name):
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO botforclone (token, admin_id, bot_name) VALUES (?, ?, ?)', (token, admin_id, bot_name))
    conn.commit()
    conn.close()

def save_bot_location(location):
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE botforclone SET location = ? WHERE id = (SELECT MAX(id) FROM botforclone)', (location,))
    conn.commit()
    conn.close()

def get_bot_location():
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT location FROM botforclone ORDER BY id DESC LIMIT 1')
    location = cursor.fetchone()[0]
    conn.close()
    return location

def get_all_bots():
    conn = sqlite3.connect('botmanager.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM botforclone')
    bots = cursor.fetchall()
    conn.close()
    return bots