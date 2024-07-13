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
    await message.answer_photo(photo="AgACAgIAAxkBAAM0ZovpRP0tUxK4RnzpMBB_AAFD5s4wAAIo4DEbQvpgSJVdwV7ynw6BAQADAgADeAADNQQ")
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! Это бот для работы с клиентами Hanoi 73. Выберите команду", reply_markup=kb.start)

@router.callback_query(F.data == "to_main")
async def to_main(callback: CallbackQuery):
    await callback.message.answer("Вы вернулись в раздел Меню", reply_markup=await kb.menu())

@router.message(F.text == "Режим работы")
async def work_time(message: Message):
    await message.answer("Ежедневно с 10:00 до 22:00 без выходных")
    
@router.message(F.text == "Расположение")
async def location(message: Message):
    await message.answer("ТРЦ Аквамолл, Московское шоссе д. 108, 2 этаж, фуд-корт, кафе «HANOI вьетнамская кухня»", reply_markup=kb.location)
    
@router.message(F.text == "Условия доставки")
async def delivery_conditions(message: Message):
    await message.answer("Доставка осуществляется с 10:00 до 21:30. \nМинимальная сумма для заказа от 1500руб. \nДоставка платная: 150руб. к сумме заказа. \nЧтобы уточнить, можете связать с менеджером", reply_markup=kb.manager)
    
@router.message(F.text == "Меню")
async def press_menu(message: Message):
    await message.answer("Вы выбрали раздел Меню", reply_markup=await kb.menu())

@router.callback_query(F.data == "menu_1")
async def soups(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANhZoxJiN7Y7dv8Mj8vMiBBhmrJIvsAAkzgMRtC-mhIDkhsQqnxwQUBAAMCAAN5AAM1BA", caption="Супы.", reply_markup=await kb.soups())

@router.callback_query(F.data == "menu_2")
async def soups(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANjZoxJlTMWtn0wzMo9VzAVtOD1lx4AAk7gMRtC-mhIglIXKdzFzLMBAAMCAAN5AAM1BA", caption="Вторые.")

@router.callback_query(F.data == "menu_3")
async def soups(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANlZoxJoiCbMeDXt0olY8STHghcOWgAAk_gMRtC-mhI34ENIRcxj1MBAAMCAAN5AAM1BA", caption="Закуски.")

@router.callback_query(F.data == "menu_4")
async def soups(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANnZoxJqYW3hdWLGkWuON6Ke7fL_dYAAlDgMRtC-mhIW1-AYG0LBc4BAAMCAAN5AAM1BA", caption="Напитки.")

@router.message(F.text == "Контакты")
async def press_contacts(message: Message):
    await message.answer("Если есть другие вопросы, то можете связаться с нашим менеджером! Если есть претензии по работе бота, внизу есть тг разработчика", reply_markup=kb.contacts)
    
"""
Списки фоток по ID
Лого кафешки - AgACAgIAAxkBAAM0ZovpRP0tUxK4RnzpMBB_AAFD5s4wAAIo4DEbQvpgSJVdwV7ynw6BAQADAgADeAADNQQ
Меню:
Супы - AgACAgIAAxkBAANhZoxJiN7Y7dv8Mj8vMiBBhmrJIvsAAkzgMRtC-mhIDkhsQqnxwQUBAAMCAAN5AAM1BA
Вторые - AgACAgIAAxkBAANjZoxJlTMWtn0wzMo9VzAVtOD1lx4AAk7gMRtC-mhIglIXKdzFzLMBAAMCAAN5AAM1BA
Закуски - AgACAgIAAxkBAANlZoxJoiCbMeDXt0olY8STHghcOWgAAk_gMRtC-mhI34ENIRcxj1MBAAMCAAN5AAM1BA
Напитки - AgACAgIAAxkBAANnZoxJqYW3hdWLGkWuON6Ke7fL_dYAAlDgMRtC-mhIW1-AYG0LBc4BAAMCAAN5AAM1BA
"""