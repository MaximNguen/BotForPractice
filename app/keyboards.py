from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Меню')],
    [KeyboardButton(text='Корзина')],
    [KeyboardButton(text='Контакты')],
    [KeyboardButton(text="Регистрация")]
], resize_keyboard=True, input_field_placeholder="Выберите команду...")

catalog = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Супы", callback_data="soup")],
    [InlineKeyboardButton(text="Вторые", callback_data="wok")],
    [InlineKeyboardButton(text="Закуски", callback_data="snacks")]
])

get_number = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Отправить номер телефона", request_contact=True)]
])