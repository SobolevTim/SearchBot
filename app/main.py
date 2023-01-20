import logging
import time
from datetime import datetime

from aiogram.utils import executor

from create_bot import dp
from handlers import user
from db import db

date = datetime.now().strftime('%d_%H-%M')
logging.basicConfig(level=logging.INFO, filename=f'log-{date}.txt')

async def start_bot(_):
    print('starting bot')
    logging.warning(f'starting bot, {time.asctime()}')
    db.sql_start()

async def stop_bot(_):
    print('bot offline')
    logging.warning(f'Bot offline, {time.asctime()}')
    db.sql_stop()

user.register_msg_from_user(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_bot, on_shutdown=stop_bot)