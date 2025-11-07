from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def start_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Add birthday"), KeyboardButton(text="Delete last enter birthday")],
            [KeyboardButton(text="List birthdays"), KeyboardButton(text="Settings", message="settings")], [KeyboardButton(text="Help")]
        ],
        resize_keyboard=True
    )
    return keyboard


def settings_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Configure notifications")
    return kb.as_markup(resize_keyboard=True)