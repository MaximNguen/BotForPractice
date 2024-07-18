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
async def soups_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANhZoxJiN7Y7dv8Mj8vMiBBhmrJIvsAAkzgMRtC-mhIDkhsQqnxwQUBAAMCAAN5AAM1BA", reply_markup=await kb.soups())


@router.callback_query(F.data=="soup_multi_1")
async def soups_pho_bo(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBMmaT99h9DOtRo-awcvFsPbXicKqpAAJL3DEb4WqhSMuXXZukS90aAQADAgADeAADNQQ", reply_markup=await kb.pho_bo())

@router.callback_query(F.data=="soup_multi_2")
async def soups_mien_bo(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBMmaT99h9DOtRo-awcvFsPbXicKqpAAJL3DEb4WqhSMuXXZukS90aAQADAgADeAADNQQ", reply_markup=await kb.mien_bo())
    
@router.callback_query(F.data=="soup_multi_11")
async def soups_bun_bo(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBMmaT99h9DOtRo-awcvFsPbXicKqpAAJL3DEb4WqhSMuXXZukS90aAQADAgADeAADNQQ", reply_markup=await kb.bun_bo())

@router.callback_query(F.data=="soup_multi_6")
async def soups_tom_yum(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBl2aWx7rWSY-geSxSt4qBCN_fLQzIAAK23TEbu6i5SCIduFuyC-1oAQADAgADeAADNQQ", reply_markup=await kb.tom_yum())
    
@router.callback_query(F.data=="soup_multi_9")
async def soups_pho_ga(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBNmaT999QpsMp9EVve-6Bs3V3WHRdAAJN3DEb4WqhSBcu-p7g1idIAQADAgADeAADNQQ", reply_markup=await kb.pho_ga())


@router.callback_query(F.data == "menu_2")
async def woks_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANjZoxJlTMWtn0wzMo9VzAVtOD1lx4AAk7gMRtC-mhIglIXKdzFzLMBAAMCAAN5AAM1BA", reply_markup=await kb.woks())

@router.callback_query(F.data == "wok_multi_13")
async def woks_com_rang(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBtmaZUmwv7lg1MYkxKbhLAh9lvRDTAAJR3DEbMnfISLQAAUUOCIvmJAEAAwIAA3gAAzUE", reply_markup=await kb.com_rang())
    
@router.callback_query(F.data == "wok_multi_18")
async def woks_mien_sao(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBuGaZUnBwaQj-6Ac8ndoOJRgZ0VLgAAJS3DEbMnfISOJGdPCy48BCAQADAgADeAADNQQ", reply_markup=await kb.mien_sao())
    
@router.callback_query(F.data == "wok_multi_22")
async def woks_mi_sao(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBumaZUnKB9OcveA9ScZpuYKz5w6S9AAJT3DEbMnfISH_gqwE4xhraAQADAgADeAADNQQ", reply_markup=await kb.mi_sao())

@router.callback_query(F.data == "wok_multi_26")
async def woks_pho_sao(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBvGaZUnWrrQ1HeikIuRVEm_E-MWbKAAJU3DEbMnfISOrnuTbXOsYpAQADAgADeAADNQQ", reply_markup=await kb.pho_sao())


@router.callback_query(F.data == "menu_3")
async def snacks_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANlZoxJoiCbMeDXt0olY8STHghcOWgAAk_gMRtC-mhI34ENIRcxj1MBAAMCAAN5AAM1BA", caption="Закуски.", reply_markup=await kb.snacks())

@router.callback_query(F.data == "snack_multi_31")
async def snacks_nem(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBvmaZUyKv8dlimi-hytzEFk9UpLH8AAJX3DEbMnfISCbsGX13gHYeAQADAgADeAADNQQ", reply_markup=await kb.nem())


@router.callback_query(F.data == "menu_4")
async def drinks_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAANnZoxJqYW3hdWLGkWuON6Ke7fL_dYAAlDgMRtC-mhIW1-AYG0LBc4BAAMCAAN5AAM1BA", caption="Напитки.", reply_markup=await kb.drinks())

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
Фо Бо, Миен Бо, Бун Бо - AgACAgIAAxkBAAIBMmaT99h9DOtRo-awcvFsPbXicKqpAAJL3DEb4WqhSMuXXZukS90aAQADAgADeAADNQQ
Фо Га - AgACAgIAAxkBAAIBNmaT999QpsMp9EVve-6Bs3V3WHRdAAJN3DEb4WqhSBcu-p7g1idIAQADAgADeAADNQQ
Том Ям - AgACAgIAAxkBAAIBl2aWx7rWSY-geSxSt4qBCN_fLQzIAAK23TEbu6i5SCIduFuyC-1oAQADAgADeAADNQQ
Кым Ранг - AgACAgIAAxkBAAIBtmaZUmwv7lg1MYkxKbhLAh9lvRDTAAJR3DEbMnfISLQAAUUOCIvmJAEAAwIAA3gAAzUE
Миен Сао -AgACAgIAAxkBAAIBuGaZUnBwaQj-6Ac8ndoOJRgZ0VLgAAJS3DEbMnfISOJGdPCy48BCAQADAgADeAADNQQ
Ми Сао - AgACAgIAAxkBAAIBumaZUnKB9OcveA9ScZpuYKz5w6S9AAJT3DEbMnfISH_gqwE4xhraAQADAgADeAADNQQ
Фо Сао - AgACAgIAAxkBAAIBvGaZUnWrrQ1HeikIuRVEm_E-MWbKAAJU3DEbMnfISOrnuTbXOsYpAQADAgADeAADNQQ
Нэм - AgACAgIAAxkBAAIBvmaZUyKv8dlimi-hytzEFk9UpLH8AAJX3DEbMnfISCbsGX13gHYeAQADAgADeAADNQQ
"""