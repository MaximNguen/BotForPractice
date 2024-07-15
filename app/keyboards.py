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
    all_foods1 = await get_foods()
    keyboard = InlineKeyboardBuilder()
    check_same = []
    for soup in all_foods:
        check_same.append(soup.name)
    check_multi = []
    for every_soup in all_foods1:
        if every_soup.category == "Супы" and check_same.count(every_soup.name) == 1:
            keyboard.add(InlineKeyboardButton(text=f"{every_soup.name} | {every_soup.size} | {every_soup.price}", callback_data=f"soup_single_{every_soup.id}"))
        elif every_soup.category == "Супы" and check_same.count(every_soup.name) >1 and every_soup.name not in check_multi:
            keyboard.add(InlineKeyboardButton(text=f"{every_soup.name}", callback_data=f"soup_multi_{every_soup.id}"))
            check_multi.append(every_soup.name)
    keyboard.add(InlineKeyboardButton(text="Вернуться к меню", callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def woks():
    all_foods = await get_foods()
    all_foods1 = await get_foods()
    keyboard = InlineKeyboardBuilder()
    check_same = []
    for wok in all_foods:
        check_same.append(wok.name)
    check_multi = []
    for every_wok in all_foods1:
        if every_wok.category == "Вторые" and check_same.count(every_wok.name) == 1:
            keyboard.add(InlineKeyboardButton(text=f"{every_wok.name} | {every_wok.size} | {every_wok.price}", callback_data=f"wok_single_{every_wok.id}"))
        elif every_wok.category == "Вторые" and check_same.count(every_wok.name) > 1 and every_wok.name not in check_multi:
            keyboard.add(InlineKeyboardButton(text=f"{every_wok.name}", callback_data=f"wok_multi_{every_wok.id}"))
            check_multi.append(every_wok.name)
    keyboard.add(InlineKeyboardButton(text="Вернуться к меню", callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def snacks():
    all_foods = await get_foods()
    all_foods1 = await get_foods()
    keyboard = InlineKeyboardBuilder()
    check_same = []
    for snack in all_foods:
        check_same.append(snack.name)
    check_multi = []
    for every_snack in all_foods1:
        if every_snack.category == "Закуски" and check_same.count(every_snack.name) == 1:
            keyboard.add(InlineKeyboardButton(text=f"{every_snack.name} | {every_snack.size} | {every_snack.price}", callback_data=f"snack_single_{every_snack.id}"))
        elif every_snack.category == "Закуски" and check_same.count(every_snack.name) > 1 and every_snack.name not in check_multi:
            keyboard.add(InlineKeyboardButton(text=f"{every_snack.name}", callback_data=f"snack_multi_{every_snack.id}")) 
            check_multi.append(every_snack.name)
    keyboard.add(InlineKeyboardButton(text="Вернуться к меню", callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

async def drinks():
    all_foods = await get_foods()
    keyboard = InlineKeyboardBuilder()
    for every_drink in all_foods:
        if every_drink.category == "Напитки":
            keyboard.add(InlineKeyboardButton(text=f"{every_drink.name} | {every_drink.size} | {every_drink.price}", callback_data=f"drink_single_{every_drink.id}"))
    keyboard.add(InlineKeyboardButton(text="Вернуться к меню", callback_data='to_main'))
    return keyboard.adjust(2).as_markup()

        