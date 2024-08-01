from aiogram import Router, F, Bot
import asyncio
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import time

import app.keyboards as kb
import app.database.requests as rq
from config import TOKEN

bot = Bot(token=TOKEN)

router = Router()

msg_delete = None

class Order(StatesGroup):
    name = State()
    number = State()
    address = State()
    comment = State()


check_words = ["Режим работы", 'Расположение', 'Условия доставки', "Меню", "Корзина", "Контакты", "/start"]
delete_allow_status = True


"""@router.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"ID - {message.photo[-1].file_id}")"""

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_photo(photo="AgACAgIAAxkBAAM0ZovpRP0tUxK4RnzpMBB_AAFD5s4wAAIo4DEbQvpgSJVdwV7ynw6BAQADAgADeAADNQQ")
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! Это бот для работы с клиентами Hanoi 73. Выберите команду", reply_markup=kb.start)

@router.callback_query(F.data == "to_main")
async def to_main(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer("Вы вернулись в раздел Меню", reply_markup=await kb.menu())
    msg_delete = msg.message_id

@router.message(F.text == "Режим работы")
async def work_time(message: Message):
    await message.answer(text="Ежедневно с 10:00 до 22:00 без выходных")
    
@router.message(F.text == "Расположение")
async def location(message: Message):
    await message.answer("ТРЦ Аквамолл, Московское шоссе д. 108, 2 этаж, фуд-корт, кафе «HANOI вьетнамская кухня»", reply_markup=kb.location)
    
@router.message(F.text == "Условия доставки")
async def delivery_conditions(message: Message):
    await message.answer("Доставка осуществляется с 10:00 до 21:30. \nМинимальная сумма для заказа от 1500руб. \nДоставка платная: 150руб. к сумме заказа. \nЧтобы уточнить, можете связать с менеджером", reply_markup=kb.manager)
    
@router.message(F.text == "Меню")
async def press_menu(message: Message):
    await message.answer("Вы выбрали раздел Меню. Выберите интересующее блюдо, чтобы добавить в корзину. Также прочитайте условия доставки, иначе ваш заказ будет отменен", reply_markup=await kb.menu())

@router.message(F.text == "Корзина")
async def basket(message: Message):
    check_cart = await rq.get_carts()
    userId = str(message.from_user.id)
    if userId in check_cart:
        msg_cart = ''
        check_name = await rq.get_carts_name(message.from_user.id)
        check_size = await rq.get_carts_size(message.from_user.id)
        check_price = await rq.get_carts_price(message.from_user.id)
        check_add = await rq.get_carts_add(message.from_user.id)
        for i in range(len(check_name)):
            if check_add[i] == "None":
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}'
            else:
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]} | {check_add[i]}'
        msg_cart += f"\nСумма заказа составляет {sum(check_price)}р"
        if sum(check_price) < 1500:
            msg_cart += f"\nВам не хватает {1500 - sum(check_price)}р отправки заказа"
            await message.answer(text=msg_cart, reply_markup=await kb.clear_basket())
        else:
            msg_cart += f"\nУ вас достаточная сумма заказа для отправки"
            await message.answer(text=msg_cart, reply_markup=await kb.send_order())
    else:
        await message.answer("Корзина пуста")

@router.callback_query(F.data == "basket")
async def basket_data(callback: CallbackQuery):
    check_cart = await rq.get_carts()
    userId = str(callback.from_user.id)
    if userId in check_cart:
        msg_cart = ''
        check_name = await rq.get_carts_name(callback.from_user.id)
        check_size = await rq.get_carts_size(callback.from_user.id)
        check_price = await rq.get_carts_price(callback.from_user.id)
        check_add = await rq.get_carts_add(callback.from_user.id)
        for i in range(len(check_name)):
            if check_add[i] == "None":
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}'
            else:
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]} | {check_add[i]}'
        msg_cart += f"\nСумма заказа составляет {sum(check_price)}р"
        if sum(check_price) < 1500:
            msg_cart += f"\nВам не хватает {1500 - sum(check_price)}р отправки заказа"
            await callback.message.answer(text=msg_cart, reply_markup=await kb.clear_basket())
        else:
            msg_cart += f"\nУ вас достаточная сумма заказа для отправки"
            await callback.message.answer(text=msg_cart, reply_markup=await kb.send_order())
    else:
        await callback.message.answer("Корзина пуста")


@router.callback_query(F.data == "clear")
async def clear_busket(callback: CallbackQuery):
    await rq.delete_cart_foods(callback.from_user.id)
    await callback.message.answer("Корзина очищена")    

@router.callback_query(F.data == "send_order")
async def get_costumer_name(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Order.name)
    await callback.message.answer("Введите ваше имя")
    
@router.message(Order.name)
async def get_costumer_number(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Order.number)
    await message.answer("Введите ваш номер телефона (Просим вас внимательно ввести номер телефона, если номер неверно введен, то ответный звонок вы не получите для подтверждения заказа, следовательно вас заказ будет отменен)")
    
@router.message(Order.number) 
async def get_costumer_comment(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await state.set_state(Order.address)
    await message.answer('Напишите свой адрес (Если самовызов - напишите "Самовызов")')
    
@router.message(Order.address) 
async def get_costumer_comment(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Order.comment)
    await message.answer("Напишите свой комментарий (Время доставки - во сколько вы подойдете забрать заказ, если самовызов; убрать какой-то ингрендиент из какого-то блюда и т. д.)")

@router.message(Order.comment)
async def gone_order(message: Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    msg_cart = ''
    check_name = await rq.get_carts_name(message.from_user.id)
    check_size = await rq.get_carts_size(message.from_user.id)
    check_price = await rq.get_carts_price(message.from_user.id)
    check_add = await rq.get_carts_add(message.from_user.id)
    for i in range(len(check_name)):
        if check_add[i] == "None":
            msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р'
        else:
            msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р | {check_add[i]}'
    msg_cart += f"\nСумма заказа составляет {sum(check_price)}р"
    await message.answer(text=f"{msg_cart}\nВаше имя - {data['name']}\nВаш номер телефона - {data['number']}\nАдрес доставки - {data['address']}\nВаш комментарий - {data['comment']}", reply_markup=await kb.confirm_order())

@router.callback_query(F.data == "confirm_order")
async def confirming(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_time = time.time()
    time_pieces = time.localtime(current_time)
    time_info = f'{time_pieces.tm_mday}.{time_pieces.tm_mon}.{time_pieces.tm_year} | {time_pieces.tm_hour}:{time_pieces.tm_min}:{time_pieces.tm_sec}'
    msg_cart = ''
    check_name = await rq.get_carts_name(callback.from_user.id)
    check_size = await rq.get_carts_size(callback.from_user.id)
    check_price = await rq.get_carts_price(callback.from_user.id)
    check_add = await rq.get_carts_add(callback.from_user.id)
    for i in range(len(check_name)):
        if check_add[i] == "None":
            msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р'
        else:
            msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р | {check_add[i]}'
    msg_cart += f"\nСумма заказа составляет {sum(check_price)}р"
    await rq.add_order(time_info, callback.message.from_user.id, data['name'], data['number'], data['address'], data['comment'], msg_cart, str(sum(check_price)))
    await bot.send_message(text=f"\n{msg_cart}\nИмя - {data['name']}\nНомер телефона - {data['number']}\nАдрес доставки - {data['address']}\nКомментарий - {data['comment']}", chat_id=5109940267)
    await state.clear()
    await rq.delete_cart_foods(callback.from_user.id)
    await callback.message.answer("Заказ был передан на обработку")

@router.callback_query(F.data == "clear_state")
async def clearning_state(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Данные очищены, можете снова их вводить")
  
@router.callback_query(F.data == "menu_1")
async def soups_answer(callback: CallbackQuery):
    global msg_delete
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAANhZoxJiN7Y7dv8Mj8vMiBBhmrJIvsAAkzgMRtC-mhIDkhsQqnxwQUBAAMCAAN5AAM1BA", reply_markup=await kb.soups())
    msg_delete = msg.message_id
    

@router.callback_query(F.data=="soup_multi_1")
async def soups_pho_bo(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBMmaT99h9DOtRo-awcvFsPbXicKqpAAJL3DEb4WqhSMuXXZukS90aAQADAgADeAADNQQ", reply_markup=await kb.pho_bo())
    msg_delete = msg.message_id
    
@router.callback_query(F.data=="soup_multi_2")
async def soups_mien_bo(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBMmaT99h9DOtRo-awcvFsPbXicKqpAAJL3DEb4WqhSMuXXZukS90aAQADAgADeAADNQQ", reply_markup=await kb.mien_bo())
    msg_delete = msg.message_id
    
@router.callback_query(F.data=="soup_multi_11")
async def soups_bun_bo(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBMmaT99h9DOtRo-awcvFsPbXicKqpAAJL3DEb4WqhSMuXXZukS90aAQADAgADeAADNQQ", reply_markup=await kb.bun_bo())
    msg_delete = msg.message_id

@router.callback_query(F.data=="soup_multi_6")
async def soups_tom_yum(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBl2aWx7rWSY-geSxSt4qBCN_fLQzIAAK23TEbu6i5SCIduFuyC-1oAQADAgADeAADNQQ", reply_markup=await kb.tom_yum())
    msg_delete = msg.message_id
    
@router.callback_query(F.data=="soup_multi_9")
async def soups_pho_ga(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBNmaT999QpsMp9EVve-6Bs3V3WHRdAAJN3DEb4WqhSBcu-p7g1idIAQADAgADeAADNQQ", reply_markup=await kb.pho_ga())
    msg_delete = msg.message_id

@router.callback_query(F.data =="soup_multi_5")
async def soups_sot_vang(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIEIWaevIZ2vttQBRC5ugi3OU7P8xRgAAJN5zEb5sL5SJ_zh7A5m3D_AQADAgADeAADNQQ", reply_markup=await kb.sot_vang())
    msg_delete = msg.message_id

@router.callback_query(F.data =="soup_multi_8")
async def soups_sot_vang(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIEH2aevGRwGyXMn1kVUbYLm6WjMmCuAAJM5zEb5sL5SMFrPvBMSspXAQADAgADeAADNQQ", reply_markup=await kb.pho_sot_vang())
    msg_delete = msg.message_id


@router.callback_query(F.data == "menu_2")
async def woks_answer(callback: CallbackQuery):
    global msg_delete
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAANjZoxJlTMWtn0wzMo9VzAVtOD1lx4AAk7gMRtC-mhIglIXKdzFzLMBAAMCAAN5AAM1BA", reply_markup=await kb.woks())
    msg_delete = msg.message_id
    
@router.callback_query(F.data == "wok_multi_13")
async def woks_com_rang(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBtmaZUmwv7lg1MYkxKbhLAh9lvRDTAAJR3DEbMnfISLQAAUUOCIvmJAEAAwIAA3gAAzUE", reply_markup=await kb.com_rang())
    msg_delete = msg.message_id
    
@router.callback_query(F.data == "wok_multi_18")
async def woks_mien_sao(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBuGaZUnBwaQj-6Ac8ndoOJRgZ0VLgAAJS3DEbMnfISOJGdPCy48BCAQADAgADeAADNQQ", reply_markup=await kb.mien_sao())
    msg_delete = msg.message_id
    
@router.callback_query(F.data == "wok_multi_22")
async def woks_mi_sao(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBumaZUnKB9OcveA9ScZpuYKz5w6S9AAJT3DEbMnfISH_gqwE4xhraAQADAgADeAADNQQ", reply_markup=await kb.mi_sao())
    msg_delete = msg.message_id

@router.callback_query(F.data == "wok_multi_26")
async def woks_pho_sao(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBvGaZUnWrrQ1HeikIuRVEm_E-MWbKAAJU3DEbMnfISOrnuTbXOsYpAQADAgADeAADNQQ", reply_markup=await kb.pho_sao())
    msg_delete = msg.message_id

@router.callback_query(F.data == "wok_multi_16")
async def woks_bun_nem(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIESWaewfuK_Sbr-uCLy8aHqQ1x83bZAAJk5zEb5sL5SDOluvb6oVovAQADAgADeAADNQQ", reply_markup=await kb.bun_nem())
    msg_delete = msg.message_id


@router.callback_query(F.data == "menu_3")
async def snacks_answer(callback: CallbackQuery):
    global msg_delete
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAANlZoxJoiCbMeDXt0olY8STHghcOWgAAk_gMRtC-mhI34ENIRcxj1MBAAMCAAN5AAM1BA", reply_markup=await kb.snacks())
    msg_delete = msg.message_id
    
@router.callback_query(F.data == "snack_multi_31")
async def snacks_nem(callback: CallbackQuery):
    global msg_delete
    if msg_delete:
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAAIBvmaZUyKv8dlimi-hytzEFk9UpLH8AAJX3DEbMnfISCbsGX13gHYeAQADAgADeAADNQQ", reply_markup=await kb.nem())
    msg_delete = msg.message_id


@router.callback_query(F.data == "menu_4")
async def drinks_answer(callback: CallbackQuery):
    global msg_delete
    msg = await callback.message.answer_photo(photo="AgACAgIAAxkBAANnZoxJqYW3hdWLGkWuON6Ke7fL_dYAAlDgMRtC-mhIW1-AYG0LBc4BAAMCAAN5AAM1BA", reply_markup=await kb.drinks())
    msg_delete = msg.message_id
    

@router.callback_query(F.data.startswith("single_"))
async def pick_food(callback: CallbackQuery):
    all_foods = await rq.get_foods()
    for food in all_foods:
        if int(callback.data.split("_")[2]) == int(food.id):
            userId = str(callback.from_user.id)
            await rq.add_food_to_cart(userId, food.name, food.price, food.size, food.add)
            global msg_delete
            if food.add == "None":
                if msg_delete:
                    await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
                msg = await callback.message.answer(text=f"{food.name} | {food.size} | {food.price}р . Перенесен в корзину", reply_markup=await kb.after_pick(callback.data.split("_")[2]))
                msg_delete = msg.message_id
            else:
                if msg_delete:
                    await bot.delete_message(chat_id=callback.message.chat.id, message_id=msg_delete)
                msg = await callback.message.answer(f"{food.name} | {food.size} | {food.price}р | {food.add}. Перенесен в корзину", reply_markup=await kb.after_pick(callback.data.split("_")[2]))
                msg_delete = msg.message_id

@router.message(F.text == "Контакты")
async def press_contacts(message: Message):
    await message.answer("Если есть другие вопросы, то можете связаться с нашим менеджером! Если есть претензии по работе бота, внизу есть тг разработчика", reply_markup=kb.contacts)
    
@router.message(F.text) 
async def delete_weird_message_text(message: Message):
    if (delete_allow_status == True):
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


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
Фо Шот Ванг - AgACAgIAAxkBAAIEH2aevGRwGyXMn1kVUbYLm6WjMmCuAAJM5zEb5sL5SMFrPvBMSspXAQADAgADeAADNQQ
Шот Ванг - AgACAgIAAxkBAAIEIWaevIZ2vttQBRC5ugi3OU7P8xRgAAJN5zEb5sL5SJ_zh7A5m3D_AQADAgADeAADNQQ
Том Ям - AgACAgIAAxkBAAIBl2aWx7rWSY-geSxSt4qBCN_fLQzIAAK23TEbu6i5SCIduFuyC-1oAQADAgADeAADNQQ
Кым Ранг - AgACAgIAAxkBAAIBtmaZUmwv7lg1MYkxKbhLAh9lvRDTAAJR3DEbMnfISLQAAUUOCIvmJAEAAwIAA3gAAzUE
Миен Сао -AgACAgIAAxkBAAIBuGaZUnBwaQj-6Ac8ndoOJRgZ0VLgAAJS3DEbMnfISOJGdPCy48BCAQADAgADeAADNQQ
Ми Сао - AgACAgIAAxkBAAIBumaZUnKB9OcveA9ScZpuYKz5w6S9AAJT3DEbMnfISH_gqwE4xhraAQADAgADeAADNQQ
Бун Нэм - AgACAgIAAxkBAAIESWaewfuK_Sbr-uCLy8aHqQ1x83bZAAJk5zEb5sL5SDOluvb6oVovAQADAgADeAADNQQ
Фо Сао - AgACAgIAAxkBAAIBvGaZUnWrrQ1HeikIuRVEm_E-MWbKAAJU3DEbMnfISOrnuTbXOsYpAQADAgADeAADNQQ
Нэм - AgACAgIAAxkBAAIBvmaZUyKv8dlimi-hytzEFk9UpLH8AAJX3DEbMnfISCbsGX13gHYeAQADAgADeAADNQQ
"""