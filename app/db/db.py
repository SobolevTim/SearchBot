import sqlite3 as sql
import logging

# from create_bot import bot

def sql_start():
    global base, cur
    base = sql.connect('bot.db')
    cur = base.cursor()
    if base:
        print('Date base connected')
        logging.warning('Date base connected')
    base.execute('''CREATE TABLE IF NOT EXISTS bot_file(
                 file_name TEXT NOT NULL,
                 file_cash TEXT NOT NULL)''')
    base.commit()

async def sql_add_file(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO bot_file(file_name, file_cash) VALUES(?, ?)', tuple(data.values()))
        base.commit()

async def sql_send_photo(text):
    try:
        cur.execute('SELECT file_cash FROM bot_file WHERE file_name = ?', (text,))
        res = cur.fetchone()[0]
        return res
    except TypeError:
        logging.warning(f'In Database not found file with id: {text}')
        return False

async def sql_list_file():
    cur.execute('SELECT file_name FROM bot_file')
    records = cur.fetchall()
    res = []
    for i in records:
        res.append(i[0])
    return res
        


def sql_stop():
    base.close()