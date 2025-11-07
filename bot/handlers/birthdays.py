from datetime import datetime
import logging
from aiogram import F, Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from text import ENTER_BIRTHDAY_DAY_EN, ENTER_BIRTHDAY_MONTH_EN, ENTER_BIRTHDAY_NAME_EN, ENTER_BIRTHDAY_YEAR_EN
from keyboards.birthdays import add_birthday_keyboard
from keyboards.start import start_keyboard
from keyboards.simple_row import make_row_keyboard


logging.basicConfig(level=logging.INFO)
router = Router()


class BirthdayCreation(StatesGroup):
    year = State()
    month = State()
    day = State()
    name = State()


@router.message(StateFilter(None), F.text.lower() == "add birthday")
@router.message(StateFilter(None), Command("add"))
async def cmd_birthday_add(message: Message, state: FSMContext):
    await message.answer(
        text=ENTER_BIRTHDAY_YEAR_EN,
        reply_markup=add_birthday_keyboard()
    )
    # Устанавливаем пользователю состояние "выбирает год"
    await state.set_state(BirthdayCreation.year)


def is_year_validate(year: str) -> bool:
    try:
        if int(year) > datetime.now().year:
            raise Exception("The introduced year has not yet arrived")
    except ValueError:
        return ValueError("Year is not valid")
    else:
        return True


@router.message(
    BirthdayCreation.year,
)
async def introduce_year(message: Message, state: FSMContext):
    try:
        is_year_validate(message.text)
    except Exception as e:
        logging.error(e)
        await message.answer(
            text=f"{e}. {ENTER_BIRTHDAY_YEAR_EN}",
            reply_markup=add_birthday_keyboard()
        )
        return
    await state.update_data(year=message.text.lower())
    await message.answer(
        text=ENTER_BIRTHDAY_MONTH_EN
    )
    await state.set_state(BirthdayCreation.month)


async def is_month_validate(month: str, state: FSMContext) -> bool:
    try:
        state_data = await state.get_data()
        state_year = int(state_data.get("year"))
        state_date = datetime(year=int(state_year), month=int(month), day=1)
        if state_date > datetime.now():
            raise Exception("The introduced month has not yet arrived")
    except ValueError:
        raise ValueError("Month is not valid")
    return True


@router.message(
    BirthdayCreation.month,
)
async def introduce_month(message: Message, state: FSMContext):
    try:
        await is_month_validate(message.text, state)
    except Exception as e:
        await message.answer(
            text=f"{e}. {ENTER_BIRTHDAY_MONTH_EN}",
            reply_markup=add_birthday_keyboard()
        )
        return
    await state.update_data(month=message.text.lower())
    await message.answer(
        text=ENTER_BIRTHDAY_DAY_EN,
    )
    await state.set_state(BirthdayCreation.day)


async def is_day_validate(day: str, state: FSMContext) -> bool:
    try:
        state_data = await state.get_data()
        state_month = int(state_data.get("month"))
        state_year = int(state_data.get("year"))
        state_date = datetime(int(state_year), int(state_month), int(day))
        if state_date > datetime.now():
            raise Exception("The introduced day has not yet arrived")  
    except ValueError:
        return ValueError("Month is not valid")
    return True



@router.message(
    BirthdayCreation.day,
)
async def introduce_day(message: Message, state: FSMContext):
    try:
        await is_day_validate(message.text, state=state)
    except Exception as e:
        await message.answer(
            text=f"{e}. {ENTER_BIRTHDAY_DAY_EN}",
            reply_markup=add_birthday_keyboard()
        )
        return
    await state.update_data(day=message.text.lower())
    await message.answer(
        text=ENTER_BIRTHDAY_NAME_EN,
    )
    await state.set_state(BirthdayCreation.name)


def is_name_validate(name: str) -> bool:
    try:
        if not 0 < len(name) <= 256:
            raise ValueError
    except ValueError:
        return ValueError("Name is not valid")
    return True



@router.message(
    BirthdayCreation.name,
)
async def introduce_name(message: Message, state: FSMContext):
    try:
        is_name_validate(message.text)
    except Exception as e:
        await message.answer(
            text=f"{e}. {ENTER_BIRTHDAY_NAME_EN}",
            reply_markup=add_birthday_keyboard()
        )
        return
    await state.update_data(name=message.text.lower())
    birthday_data = await state.get_data()
    logging.info(birthday_data)
    await message.answer(
        text=f"\U0001F381 <b>Successfully added birthday for {birthday_data['name']} on {birthday_data['day']}.{birthday_data['month']}.{birthday_data['year']}</b> \U0001F381",
        reply_markup=start_keyboard(),
        parse_mode='HTML'
    )
    await state.clear()
