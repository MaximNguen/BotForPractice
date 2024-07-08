from aiogram import Router, F
import asyncio
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

@router.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"ID - {message.photo[-1].file_id}")

    
@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_photo(photo='C:\Users\Maksim\Desktop\Python Projects\First pet-project\visitPhoto.jpg')
    await message.answer_photo(photo="AgACAgIAAxkBAAM0ZovpRP0tUxK4RnzpMBB_AAFD5s4wAAIo4DEbQvpgSJVdwV7ynw6BAQADAgADeAADNQQ")
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! Это бот для работы с клиентами Hanoi 73. Выберите команду", reply_markup=kb.start)
    
@router.message(F.text == "Меню")
async def press_menu(message: Message):
    await message.answer("Вы выбрали раздел Меню", reply_markup=await kb.menu())
    
@router.message(F.text == "Контакты")
async def press_contacts(message: Message):
    await message.answer("Если есть другие вопросы, то можете связаться с нашим менеджером! Если есть претензии по работе бота, внизу есть тг разработчика", reply_markup=kb.contacts)
    
"""
Списки фоток по ID
Лого кафешки - AgACAgIAAxkBAAM0ZovpRP0tUxK4RnzpMBB_AAFD5s4wAAIo4DEbQvpgSJVdwV7ynw6BAQADAgADeAADNQQ
Меню:
Супы - 
Вторые -
Закуски -
Напитки -
"""