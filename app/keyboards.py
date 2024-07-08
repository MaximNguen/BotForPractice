from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_menu

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Меню")],
    [KeyboardButton(text="Корзина")],
    [KeyboardButton(text="Контакты")],
], resize_keyboard=True, input_field_placeholder="Выберите команду...")

contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Менеджер", url="https://t.me/cafe_hanoi_73")],
    [InlineKeyboardButton(text="Разработчик", url='https://t.me/MaxLikeVolleyball')],
])

async def menu():
    all_menu = await get_menu()
    keyboard = InlineKeyboardBuilder()
    for every_menu in all_menu:
        keyboard.add(InlineKeyboardButton(text=every_menu.name, callback_data=f"menu_{every_menu.id}"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

