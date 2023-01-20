from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import db
from create_bot import bot

class FSMUser(StatesGroup):
    file_name = State()
    file = State()

async def start_command(message: Message):
    await message.answer(f'Привет, пользователь {message.from_user.first_name}')

async def start_upload_file(message: Message):
    await message.answer(f'Укажите артикул детали:')
    await FSMUser.file_name.set()

async def upload_file_name(message: Message, state: FSMContext):
    if 'отмена' in message.text.lower() or 'cancel' in message.text.lower():
        await state.finish()
        await message.answer('Загрузка отменена')
    else:
        async with state.proxy() as data:
            data['file_name'] = message.text
        await message.answer(f'Теперь загрузите файл')
        await FSMUser.next()

async def upload_file(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['file'] = message.photo[0].file_id
    await db.sql_add_file(state)
    await message.answer(f'Файл успешно загружен.')
    await state.finish()

async def download_file(message: Message):
    cash_file = await db.sql_send_photo(message.text)
    await bot.send_photo(message.chat.id, cash_file)

async def file_list(message: Message):
    res = await db.sql_list_file()
    res.sort()
    await message.answer(f'В бота загружено файлов: {len(res)}. Вот список артикулов:')
    await message.answer("\n".join(res))

# Дополнить описание в команде
async def help_command(message: Message):
    await message.answer(f'Для того чтобы найти деталь по артиклу - просто введи артикул\nДля загрузки файлов в базу телеграм воспользуйтесь командой /upload')

def register_msg_from_user(dp : Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(help_command, commands=['help'])
    dp.register_message_handler(start_upload_file, commands=['upload'])
    dp.register_message_handler(upload_file_name, state=FSMUser.file_name)
    dp.register_message_handler(upload_file, state=FSMUser.file, content_types=['photo'])
    dp.register_message_handler(file_list, commands=['list'])
    dp.register_message_handler(download_file)