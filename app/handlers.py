from aiogram import Router, F, Bot
import asyncio
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import pytz
import datetime

import app.keyboards as kb
import app.database.requests as rq
from config import TOKEN

bot = Bot(token=TOKEN)

router = Router()

allowed_time = [int(i) for i in range(10, 22)]

class Order(StatesGroup):
    name = State()
    number = State()
    address = State()
    time = State()
    comment = State()

class Order_InCafe(StatesGroup):
    name = State()
    number = State()
    time = State()
    comment = State()

check_words = ["Режим работы", 'Расположение', 'Условия доставки', "Меню", "Корзина", "Контакты", "/start"]
delete_allow_status = True


@router.message(F.photo)
async def get_photo_id(message: Message):
    await message.answer(f"ID - {message.photo[-1].file_id}")

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer_photo(photo="AgACAgIAAxkBAAMGZsWGgBOwD9C-P5bcH1MNUIvQkhwAAqLmMRs4qihKmFXHHttR-jMBAAMCAAN5AAM1BA")
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! Это бот для работы с клиентами Hanoi 73. Выберите команду", reply_markup=kb.start)

@router.callback_query(F.data == "to_main")
async def to_main(callback: CallbackQuery):
    await callback.message.answer("Вы вернулись в раздел Меню", reply_markup=await kb.menu())

@router.message(F.text == "Режим работы")
async def work_time(message: Message):
    await message.answer(text="Ежедневно с 10:00 до 22:00 без выходных")
    
@router.message(F.text == "Расположение")
async def location(message: Message):
    await message.answer("ТРЦ Аквамолл, Московское шоссе д. 108, 2 этаж, фуд-корт, кафе «HANOI вьетнамская кухня»", reply_markup=kb.location)
    
@router.message(F.text == "Условия доставки и самовызова")
async def delivery_conditions(message: Message):
    await message.answer("Доставка осуществляется с 10:00 до 21:30. \nМинимальная сумма для доставки заказа от 1500руб. \nДоставка платная: 150руб. к сумме заказа.\nСамовызов бесплатный\nЧтобы уточнить, можете связаться с менеджером", reply_markup=kb.manager)
    
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
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р'
            else:
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р | {check_add[i]}'
        msg_cart += f"\nСумма заказа составляет {sum(check_price)}р"
        if sum(check_price) < 1500:
            msg_cart += f"\nВам не хватает {1500 - sum(check_price)}р для оформления заказа на доставку, но можно оформить заказ на самовызов"
            await message.answer(text=msg_cart, reply_markup=await kb.send_order_no_delivery())
        else:
            msg_cart += f"\nУ вас достаточная сумма для отправки заказа на доставку или самовызов"
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
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р'
            else:
                msg_cart += f'\n{check_name[i]} | {check_size[i]} | {check_price[i]}р | {check_add[i]}'
        msg_cart += f"\nСумма заказа составляет {sum(check_price)}р"
        if sum(check_price) < 1500:
            msg_cart += f"\nВам не хватает {1500 - sum(check_price)}р для оформления заказа на доставку, но можно оформить заказ на самовызов"
            await callback.message.answer(text=msg_cart, reply_markup=await kb.send_order_no_delivery())
        else:
            msg_cart += f"\nУ вас достаточная сумма для отправки заказа на доставку или самовызов"
            await callback.message.answer(text=msg_cart, reply_markup=await kb.send_order())
    else:
        await callback.message.answer("Корзина пуста")


@router.callback_query(F.data == "clear")
async def clear_busket(callback: CallbackQuery):
    await rq.delete_cart_foods(callback.from_user.id)
    await callback.message.answer("Корзина очищена")    

@router.callback_query(F.data == "send_order")
async def get_costumer_name(callback: CallbackQuery, state: FSMContext):
    check_time_set = pytz.timezone("Europe/Samara")
    check_time = datetime.datetime.now(check_time_set)
    if int(check_time.strftime("%H")) in allowed_time:
        if int(check_time.strftime("%H")) != 21 or (int(check_time.strftime("%H")) == 21 and int(check_time.strftime("%M")) < 30):
            await state.set_state(Order.name)
            await callback.message.answer("Введите ваше имя")
        else:
            await callback.message.answer("Наше заведение на данный момент закрыт, сделайте заказ с 10:00 по 21:30")
    else:
        await callback.message.answer("Наше заведение на данный момент закрыт, сделайте заказ с 10:00 по 21:30")
    
@router.message(Order.name)
async def get_costumer_number(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Order.number)
    await message.answer("Отправьте ваш номер телефона, чтобы менеджер смог связаться с вами (Нажмите на кнопки снизу)", reply_markup=kb.send_number)
    
@router.message(Order.number, F.contact) 
async def get_costumer_address(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await state.set_state(Order.address)
    await message.answer('Напишите свой полный адрес для доставки (название улицы, номер дома, подъезд, этаж и номер квартиры)',reply_markup=kb.start)
    
@router.message(Order.address)
async def get_costumer_time(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Order.time)
    await message.answer("Напишите промежуток времени, к которому нужно доставить заказ")
    
@router.message(Order.time) 
async def get_costumer_comment(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(Order.comment)
    await message.answer("Напишите свой комментарий по поводу заказа (убрать ингредиент из какого-либо блюда и т.п.)")

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
    msg_cart += f"\nСумма заказа составляет {sum(check_price) + 150}р с учетом стоимости доставки (150р)"
    await message.answer(text=f"{msg_cart}\nВаше имя - {data['name']}\nВаш номер телефона - {data['number']}\nАдрес доставки - {data['address']}\nВремя доставки - {data['time']}\nВаш комментарий - {data['comment']}", reply_markup=await kb.confirm_order())

@router.callback_query(F.data == "confirm_order")
async def confirming(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_time_set = pytz.timezone("Europe/Samara")
    current_time = datetime.datetime.now(current_time_set)
    time_info = current_time.strftime("%Y-%m-%d %H:%M:%S")
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
    msg_cart += f"\nСумма заказа составляет {sum(check_price) + 150}р (с учетом доставки)"
    await rq.add_order(time_info, callback.message.from_user.id, data['name'], data['number'], data['address'], data['comment'], msg_cart, str(sum(check_price)))
    await bot.send_message(text=f"Доставка:\n{msg_cart}\nИмя - {data['name']}\nАдрес доставки - {data['address']}\nВремя доставки - {data['time']}\nКомментарий - {data['comment']}", chat_id=5109940267)
    await bot.send_message(text=f"+{data['number']}", chat_id=5109940267)
    await state.clear()
    await rq.delete_cart_foods(callback.from_user.id)
    await callback.message.answer("Заказ был передан на обработку")
    
    
@router.callback_query(F.data == "send_order_no_delivery")
async def get_costumer_name_in_cafe(callback: CallbackQuery, state: FSMContext):
    check_time_set = pytz.timezone("Europe/Samara")
    check_time = datetime.datetime.now(check_time_set)
    if int(check_time.strftime("%H")) in allowed_time:
        if int(check_time.strftime("%H")) != 21 or (int(check_time.strftime("%H")) == 21 and int(check_time.strftime("%M")) < 30):
            await state.set_state(Order_InCafe.name)
            await callback.message.answer("Введите ваше имя")
        else:
            await callback.message.answer("Наше заведение на данный момент закрыт, сделайте заказ с 10:00 по 21:30")
    else:
        await callback.message.answer("Наше заведение на данный момент закрыт, сделайте заказ с 10:00 по 21:30")

@router.message(Order_InCafe.name)
async def get_costumer_number_in_cafe(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Order_InCafe.number)
    await message.answer("Отправьте ваш номер телефона, чтобы менеджер смог связаться с вами (Нажмите на кнопки снизу)", reply_markup=kb.send_number)

@router.message(Order_InCafe.number, F.contact) 
async def get_costumer_address(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    await state.set_state(Order_InCafe.time)
    await message.answer('Напишите промежуток времени, к которому нужно выполнить самовызов',reply_markup=kb.start)

@router.message(Order_InCafe.time) 
async def get_costumer_comment(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    await state.set_state(Order_InCafe.comment)
    await message.answer("Напишите свой комментарий по поводу заказа (убрать ингредиент из какого-либо блюда и т.п.)")

@router.message(Order_InCafe.comment)
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
    await message.answer(text=f"{msg_cart}\nВаше имя - {data['name']}\nВаш номер телефона - {data['number']}\nВремя самовызова - {data['time']}\nВаш комментарий - {data['comment']}", reply_markup=await kb.confirm_order_no_delivery())

@router.callback_query(F.data == "confirm_order_in_cafe")
async def confirming(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_time_set = pytz.timezone("Europe/Samara")
    current_time = datetime.datetime.now(current_time_set)
    time_info = current_time.strftime("%Y-%m-%d %H:%M:%S")
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
    await rq.add_order(time_info, callback.message.from_user.id, data['name'], data['number'], f"Самовынос - {data['time']}", data['comment'], msg_cart, str(sum(check_price)))
    await bot.send_message(text=f"Самовызов:\n{msg_cart}\nИмя - {data['name']}\nНомер телефона - {data['number']}\nВремя самовызова - {data['time']}\nКомментарий - {data['comment']}", chat_id=5109940267)
    await bot.send_message(text=f"+{data['number']}", chat_id=5109940267)
    await state.clear()
    await rq.delete_cart_foods(callback.from_user.id)
    await callback.message.answer("Заказ был передан на обработку")



@router.callback_query(F.data == "clear_state_in_cafe")
async def clearning_state(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Данные очищены, можете снова их вводить")

@router.callback_query(F.data == "clear_state")
async def clearning_state(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer("Данные очищены, можете снова их вводить")
  
  
@router.callback_query(F.data == "menu_1")
async def soups_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMUZsWHFvYk1E75f43WOQABKgHejPhEAAIS3TEbT5ExSmvYg_cd8sPwAQADAgADeQADNQQ", reply_markup=await kb.soups())

@router.callback_query(F.data=="soup_multi_1")
async def soups_pho_bo(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMcZsWITtPTcHo5S3PKGHU5NqbY4TYAAiLdMRtPkTFKCmHhYrNtY2oBAAMCAAN4AAM1BA", reply_markup=await kb.pho_bo())
    
@router.callback_query(F.data=="soup_multi_2")
async def soups_mien_bo(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMcZsWITtPTcHo5S3PKGHU5NqbY4TYAAiLdMRtPkTFKCmHhYrNtY2oBAAMCAAN4AAM1BA", reply_markup=await kb.mien_bo())
    
@router.callback_query(F.data=="soup_multi_11")
async def soups_bun_bo(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMcZsWITtPTcHo5S3PKGHU5NqbY4TYAAiLdMRtPkTFKCmHhYrNtY2oBAAMCAAN4AAM1BA", reply_markup=await kb.bun_bo())

@router.callback_query(F.data=="soup_multi_6")
async def soups_tom_yum(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMkZsWJfqQl6FKoBzDSK-xmhu4rkb0AAibdMRtPkTFKo_qFYJI-WRsBAAMCAAN4AAM1BA", reply_markup=await kb.tom_yum())
    
@router.callback_query(F.data=="soup_multi_9")
async def soups_pho_ga(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMeZsWIm6OCr3nkmFiwgs38GuIV55sAAiPdMRtPkTFKDQj7q97oZX8BAAMCAAN4AAM1BA", reply_markup=await kb.pho_ga())

@router.callback_query(F.data =="soup_multi_5")
async def soups_sot_vang(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMiZsWJPBU7hkJCwZIjN_s-aiLmiWwAAiXdMRtPkTFKYWNc9PAgmZYBAAMCAAN4AAM1BA", reply_markup=await kb.sot_vang())

@router.callback_query(F.data =="soup_multi_8")
async def soups_pho_sot_vang(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMgZsWI5jX69294n9g763C9cHaLAeQAAiTdMRtPkTFKKEngsYJLbC0BAAMCAAN4AAM1BA", reply_markup=await kb.pho_sot_vang())


@router.callback_query(F.data == "menu_2")
async def woks_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMWZsWHuMTzRXsLzMcsjI5OGWt9DKgAAhrdMRtPkTFKsAQ68lxyXlQBAAMCAAN5AAM1BA", reply_markup=await kb.woks())
    
@router.callback_query(F.data == "wok_multi_13")
async def woks_com_rang(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMmZsWJ0hkjEz8fubwi0ZHDyDNYZFQAAijdMRtPkTFKfNxaR9mBosQBAAMCAAN4AAM1BA", reply_markup=await kb.com_rang())
    
@router.callback_query(F.data == "wok_multi_18")
async def woks_mien_sao(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMoZsWKC2Tq0eYPOV-aVMOyziHU2ygAAirdMRtPkTFKUDRGsnabvfABAAMCAAN4AAM1BA", reply_markup=await kb.mien_sao())
    
@router.callback_query(F.data == "wok_multi_22")
async def woks_mi_sao(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMqZsWKRUvT_SRaNn01wQQhLTd1sjQAAivdMRtPkTFK1SdC-2W_GxQBAAMCAAN4AAM1BA", reply_markup=await kb.mi_sao())

@router.callback_query(F.data == "wok_multi_26")
async def woks_pho_sao(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMuZsWKwj2qduZmdu_QZTAfLeqJ1KcAAi3dMRtPkTFK374_ePaCc0IBAAMCAAN4AAM1BA", reply_markup=await kb.pho_sao())

@router.callback_query(F.data == "wok_multi_16")
async def woks_bun_nem(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMsZsWKgFkgULvg1cY9VfyKdd4FajkAAizdMRtPkTFKo_LNn_3yEsgBAAMCAAN4AAM1BA", reply_markup=await kb.bun_nem())


@router.callback_query(F.data == "menu_3")
async def snacks_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMYZsWH9ZTO1ImaOakDc-tlMyoZdW0AAh_dMRtPkTFKPnoulK5FeJEBAAMCAAN5AAM1BA", reply_markup=await kb.snacks())
    
@router.callback_query(F.data == "snack_multi_31")
async def snacks_nem(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMwZsWK85Gw_5h8OdvDmIZKtS9_cNIAAi7dMRtPkTFK0Em0fFO4LXUBAAMCAAN4AAM1BA", reply_markup=await kb.nem())


@router.callback_query(F.data == "menu_4")
async def drinks_answer(callback: CallbackQuery):
    await callback.message.answer_photo(photo="AgACAgIAAxkBAAMaZsWIC8CUEPI_n7pgNd8lco0Di3kAAiDdMRtPkTFKUON62tButaEBAAMCAAN5AAM1BA", reply_markup=await kb.drinks())
    

@router.callback_query(F.data.startswith("single_"))
async def pick_food(callback: CallbackQuery):
    all_foods = await rq.get_foods()
    for food in all_foods:
        if int(callback.data.split("_")[2]) == int(food.id):
            userId = str(callback.from_user.id)
            await rq.add_food_to_cart(userId, food.name, food.price, food.size, food.add)
            global msg_delete
            if food.add == "None":
                await callback.message.answer(text=f"{food.name} | {food.size} | {food.price}р . Перенесен в корзину", reply_markup=await kb.after_pick(callback.data.split("_")[2]))
            else:
                await callback.message.answer(f"{food.name} | {food.size} | {food.price}р | {food.add}. Перенесен в корзину", reply_markup=await kb.after_pick(callback.data.split("_")[2]))

@router.message(F.text == "Контакты")
async def press_contacts(message: Message):
    await message.answer("Если есть другие вопросы, то можете связаться с нашим менеджером! Если есть претензии по работе бота, внизу есть тг разработчика", reply_markup=kb.contacts)
    
@router.message(F.text) 
async def delete_weird_message_text(message: Message):
    if (delete_allow_status == True):
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


"""
Списки фоток по ID
Лого кафешки - AgACAgIAAxkBAAMGZsWGgBOwD9C-P5bcH1MNUIvQkhwAAqLmMRs4qihKmFXHHttR-jMBAAMCAAN5AAM1BA
Меню:
Супы - AgACAgIAAxkBAAMUZsWHFvYk1E75f43WOQABKgHejPhEAAIS3TEbT5ExSmvYg_cd8sPwAQADAgADeQADNQQ
Вторые - AgACAgIAAxkBAAMWZsWHuMTzRXsLzMcsjI5OGWt9DKgAAhrdMRtPkTFKsAQ68lxyXlQBAAMCAAN5AAM1BA
Закуски - AgACAgIAAxkBAAMYZsWH9ZTO1ImaOakDc-tlMyoZdW0AAh_dMRtPkTFKPnoulK5FeJEBAAMCAAN5AAM1BA
Напитки - AgACAgIAAxkBAAMaZsWIC8CUEPI_n7pgNd8lco0Di3kAAiDdMRtPkTFKUON62tButaEBAAMCAAN5AAM1BA
Фо Бо, Миен Бо, Бун Бо - AgACAgIAAxkBAAMcZsWITtPTcHo5S3PKGHU5NqbY4TYAAiLdMRtPkTFKCmHhYrNtY2oBAAMCAAN4AAM1BA
Фо Га - AgACAgIAAxkBAAMeZsWIm6OCr3nkmFiwgs38GuIV55sAAiPdMRtPkTFKDQj7q97oZX8BAAMCAAN4AAM1BA
Фо Шот Ванг - AgACAgIAAxkBAAMgZsWI5jX69294n9g763C9cHaLAeQAAiTdMRtPkTFKKEngsYJLbC0BAAMCAAN4AAM1BA
Шот Ванг - AgACAgIAAxkBAAMiZsWJPBU7hkJCwZIjN_s-aiLmiWwAAiXdMRtPkTFKYWNc9PAgmZYBAAMCAAN4AAM1BA
Том Ям - AgACAgIAAxkBAAMkZsWJfqQl6FKoBzDSK-xmhu4rkb0AAibdMRtPkTFKo_qFYJI-WRsBAAMCAAN4AAM1BA
Кым Ранг - AgACAgIAAxkBAAMmZsWJ0hkjEz8fubwi0ZHDyDNYZFQAAijdMRtPkTFKfNxaR9mBosQBAAMCAAN4AAM1BA
Миен Сао - AgACAgIAAxkBAAMoZsWKC2Tq0eYPOV-aVMOyziHU2ygAAirdMRtPkTFKUDRGsnabvfABAAMCAAN4AAM1BA
Ми Сао - AgACAgIAAxkBAAMqZsWKRUvT_SRaNn01wQQhLTd1sjQAAivdMRtPkTFK1SdC-2W_GxQBAAMCAAN4AAM1BA
Бун Нэм - AgACAgIAAxkBAAMsZsWKgFkgULvg1cY9VfyKdd4FajkAAizdMRtPkTFKo_LNn_3yEsgBAAMCAAN4AAM1BA
Фо Сао - AgACAgIAAxkBAAMuZsWKwj2qduZmdu_QZTAfLeqJ1KcAAi3dMRtPkTFK374_ePaCc0IBAAMCAAN4AAM1BA
Нэм - AgACAgIAAxkBAAMwZsWK85Gw_5h8OdvDmIZKtS9_cNIAAi7dMRtPkTFK0Em0fFO4LXUBAAMCAAN4AAM1BA
"""