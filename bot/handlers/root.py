from aiogram import F, Router
from aiogram.filters import Command

from text import HELP_MESSAGE_EN, START_MESSAGE_EN
from aiogram import types
from keyboards.start import start_keyboard, settings_keyboard


router = Router()


@router.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(START_MESSAGE_EN, reply_markup=start_keyboard())


@router.message(F.text.lower() == "help")
@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer(HELP_MESSAGE_EN, reply_markup=start_keyboard())


@router.message(F.text.lower() == "settings")
@router.message(Command("settings"))
async def settings(message: types.Message):
    await message.answer("Choose setting you want to change", reply_markup=settings_keyboard())
