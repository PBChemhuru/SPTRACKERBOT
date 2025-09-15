import sqlite3

DB_NAME = 'players.db'
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            current_sp INTEGER,
            max_sp INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def add_character(user: str, name: str, level: int, sp: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO characters (user, name, level, current_sp, max_sp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user,  name.lower(), level, sp, sp))
    conn.commit()
    conn.close()

def get_characters_by_user(user:str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
            SELECT name, level, current_sp, max_sp
            FROM characters
            WHERE user= ?
        ''', (user,))
    results = cursor.fetchall()
    conn.close()
    return results
    
def get_characters():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
            SELECT name, level, current_sp, max_sp
            FROM characters  
        ''')
    results = cursor.fetchall()
    conn.close()
    return results
    
def update_character(user: str, original_name: str, new_name: str, level: int, sp: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE characters
        SET name = ?, level = ?, current_sp = ?, max_sp = ?
        WHERE user = ? AND name = ?
    ''', (new_name.lower(), level, sp, sp, user, original_name.lower()))

    conn.commit()
    conn.close()

def delete_character(user: str, name: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM characters
        WHERE user = ? AND name = ?
    ''', (user, name.lower()))

    conn.commit()
    conn.close()

def increment_all_current_sp(amount: int = 1):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE characters
            SET current_sp = MIN(current_sp + ?, max_sp)
        ''', (amount,))

        conn.commit()
        conn.close()


def get_current_sp(user: str, name: str) -> int | None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT current_sp
        FROM characters
        WHERE user = ? AND name = ?
    ''', (user, name.lower()))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
    
def get_max_sp(user: str, name: str) -> int | None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT max_sp
        FROM characters
        WHERE user = ? AND name = ?
    ''', (user, name.lower()))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None
    
def spend_sp(user: str, name: str, amount: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE characters
        SET current_sp = current_sp - ?
        WHERE user = ? AND name = ?
    ''', (amount, user, name.lower()))
    conn.commit()
    conn.close()

def regain_sp(user: str, name: str, amount: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE characters
        SET current_sp = MIN(current_sp + ?, max_sp)
        WHERE user = ? AND name = ?
    ''', (amount, user, name.lower()))
    conn.commit()
    conn.close()



def rest_user(user:str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
            UPDATE characters
            SET current_sp = max_sp
            WHERE user = ?
        ''', (user,))

    conn.commit()
    conn.close()
