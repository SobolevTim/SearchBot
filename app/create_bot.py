import os
from dotenv import load_dotenv, find_dotenv

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

load_dotenv(find_dotenv())

bot = Bot(os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

ADMIN_ID = os.getenv("ADMIN_ID")