from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_menu, get_foods

start = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Режим работы")],
    [KeyboardButton(text="Расположение")],
    [KeyboardButton(text="Условия доставки")],
    [KeyboardButton(text="Меню"),
    KeyboardButton(text="Заказать"),
    KeyboardButton(text="Корзина")],
    [KeyboardButton(text="Контакты")]
], resize_keyboard=True, input_field_placeholder="Выберите команду...")

contacts = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Менеджер", url="https://t.me/cafe_hanoi_73")],
    [InlineKeyboardButton(text="Разработчик", url='https://t.me/MaxLikeVolleyball')],
])

location = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Открыть карту", url="https://yandex.ru/maps/org/hanoi/97574318406")]
])

manager = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Менеджер', url="https://t.me/cafe_hanoi_73")]
])

async def menu():
    all_menu = await get_menu()
    keyboard = InlineKeyboardBuilder()
    for every_menu in all_menu:
        keyboard.add(InlineKeyboardButton(text=every_menu.name, callback_data=f"menu_{every_menu.id}"))
    """keyboard.add(InlineKeyboardButton(text="Вернуться к меню", callback_data='to_main'))"""
    return keyboard.adjust(2).as_markup()

async def soups():
    all_foods = await get_foods()
    keyboard = InlineKeyboardBuilder()
    check_same = []
    for soup in all_foods:
        check_same.append(soup.name)
    print(check_same)
    for every_soup in all_foods:
        print(every_soup.name) # - Эта строка не выводит на экран при нажатии кнопки Супы
        if every_soup.category == "Супы" and check_same.count(every_soup.name) < 2:
            keyboard.add(InlineKeyboardButton(text=f"{every_soup.name} | {every_soup.size} | {every_soup.price}", callback_data=f"soup_{every_soup.id}"))
    keyboard.add(InlineKeyboardButton(text="Вернуться к меню", callback_data='to_main'))
    return keyboard.adjust(2).as_markup()
            
async def woks():
    all_foods = await get_foods()
    keyboard = InlineKeyboardBuilder()
    for every_wok in all_foods:
        if every_wok.category == "Вторые":
            keyboard.add(InlineKeyboardButton(text=f"{every_wok.name} | {every_wok.size} | {every_wok.price}"))
    keyboard.add(InlineKeyboardButton(text="Вернуться к меню", callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

