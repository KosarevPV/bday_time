import logging
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from backend_client import BackendClient
from keyboards.birthdays import cancel_keyboard
from text import HELP_MESSAGE_EN, START_MESSAGE_EN
from aiogram import types
from keyboards.start import start_keyboard, settings_keyboard


router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await BackendClient(message.from_user.id).create_user(dict(message.from_user))
    await message.answer(START_MESSAGE_EN, reply_markup=start_keyboard())


@router.message(F.text.lower() == "❓ help")
@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer(HELP_MESSAGE_EN, reply_markup=start_keyboard())


@router.message(F.text.lower() == "⚙️ settings")
@router.message(Command("settings"))
async def settings(message: types.Message):
    await message.answer(
        "Choose setting you want to change", reply_markup=settings_keyboard()
    )


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "cancel")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Action canceled", reply_markup=start_keyboard())
