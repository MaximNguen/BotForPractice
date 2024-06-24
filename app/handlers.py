from aiogram import Router, Dispatcher, Bot, F
import asyncio
from aiogram.types import Message, CallbackQuery
import logging
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb

router = Router()

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}", reply_markup=kb.main)
    await message.answer("Выберите команду")

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("А?")

@router.message(F.text == "Меню")
async def menu(message: Message):
    await message.answer("Выберите блюда", reply_markup=kb.catalog)

@router.callback_query(F.data == "soup")
async def soup(callback: CallbackQuery):
    await callback.answer("Супы")
    await callback.message.answer("Тут супы типа :D", show_alert=True)

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
            @router.message(Register.number)
            async def register_number(message: Message, state: FSMContext):
                await state.update_data(number=message.text)
    

    