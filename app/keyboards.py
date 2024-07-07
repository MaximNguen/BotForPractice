from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_menu, get_menu_item

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Меню')],
    [KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Контакты')],
    [KeyboardButton(text="Регистрация")]
], resize_keyboard=True, input_field_placeholder="Выберите команду...")

get_number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
])

async def menu():
    all_menu = await get_menu()
    keyboard = InlineKeyboardBuilder()
    for every_menu in all_menu:
        keyboard.add(InlineKeyboardButton(text=every_menu.name, callback_data=f"menu_{every_menu.id}"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="go_main"))
    return keyboard.adjust(2).as_markup()

async def chosen_type(menu_id):
    all_item = await get_menu_item(menu_id)
    keyboard = InlineKeyboardBuilder()
    for item in all_item:
        keyboard.add(InlineKeyboardButton(text=item.name, callback_data=f"chosen_type_{item.category}"))
    keyboard.add(InlineKeyboardButton(text="На главную", callback_data="go_main"))
    return keyboard.adjust(2).as_markup()

