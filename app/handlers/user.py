from aiogram import Dispatcher
from aiogram.types import Message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import db
from create_bot import bot

class FSMUser(StatesGroup):
    file_name = State()
    file = State()
    del_file_name = State()

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
    if cash_file:
        await bot.send_photo(message.chat.id, cash_file)
    else:
        await message.answer('Файл с таким артикулом не найден')

async def file_list(message: Message):
    res = await db.sql_list_file()
    if len(res) != 0:
        res.sort()
        await message.answer(f'В бота загружено файлов: {len(res)}. Вот список артикулов:')
        await message.answer("\n".join(res))
    else:
        await message.answer('Файлы пока не загружены, воспользуйтесь командой /upload для загрузки')

async def cmd_delete_file(message: Message):
    await message.answer('Укажите артикул файла, который хотите удалить')
    await FSMUser.del_file_name.set()

async def delete_file(message: Message, state: FSMContext):
    if 'отмена' in message.text.lower() or 'cancel' in message.text.lower():
        await state.finish()
        await message.answer('Удаление файла отменено')
    else:
        cash_file = await db.sql_send_photo(message.text)
        if cash_file:
            await db.sql_del_file(message.text)
            await message.answer('Удаление файла прошло успешно. Для получения списка файлов воспользуйтесь командой /list')
        else:
            await message.answer('Не удалось удалить файл. Проверь правильность ввода артикула. Список артикулов можно получить командой /list')
        await state.finish()


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
    dp.register_message_handler(cmd_delete_file, commands=['delete'])
    dp.register_message_handler(delete_file, state=FSMUser.del_file_name)
    dp.register_message_handler(download_file)