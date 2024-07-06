from aiogram import Router, Dispatcher, Bot, F
import asyncio
from aiogram.types import Message, CallbackQuery
import logging
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f"Здравствуйте, {message.from_user.first_name}", reply_markup=kb.main)
    await message.answer("Выберите команду")

@router.message(F.text == "Меню")
async def menu(message: Message):
    await message.answer("Выберите блюда", reply_markup=await kb.menu())
    
@router.callback_query(F.data.startswith("chosen_type_"))
async def menu(callback: CallbackQuery):
    await callback.answer("Вы выбрали категорию")
    await callback.message.answer("Выберите блюдо", reply_markup=await kb.chosen_type(callback.data.split("_")[1]))

@router.callback_query(F.data.startswith("soup_"))
async def menu(callback: CallbackQuery):
    await callback.answer("Вы выбрали супы")
    await callback.message.answer("Выберите блюдо", reply_markup=await kb.soups(callback.data.split("_")[1]))

@router.message(F.text == "Регистрация")
async def register(message:Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer("Введите ваше имя")
    
@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Register.age)
    await message.answer("Введите ваш возраст")
    
@router.message(Register.age)
async def register_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Register.number)
    await message.answer("Введите ваш номер телефона", reply_markup=kb.get_number)

@router.message(Register.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    data = await state.get_data()
    await message.answer(f"Ваш номер {data['number']}")
