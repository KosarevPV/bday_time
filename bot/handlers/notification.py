from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from backend_client import BackendClient
from keyboards.birthdays import cancel_keyboard
from text import HELP_MESSAGE_EN, START_MESSAGE_EN
from aiogram import types
from keyboards.start import start_keyboard, settings_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.filters import Command


router = Router()


@router.message(F.text.lower() == "configure notifications")
@router.message(Command("update_notifications"))
async def update_notifications(message: types.Message):
    client = BackendClient(message.from_user.id)
    notifications = await client.get_notification()

    edit_notifications_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🕛 Day of birthday {'✅' if notifications['day_0'] else '❌'}",
                    callback_data="edit_notif_0",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"1️⃣ 1 day {'✅' if notifications['day_1'] else '❌'}",
                    callback_data="edit_notif_1",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"3️⃣ 3 days {'✅' if notifications['day_3'] else '❌'}",
                    callback_data="edit_notif_3",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"7️⃣ 7 days {'✅' if notifications['day_7'] else '❌'}",
                    callback_data="edit_notif_7",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"2️⃣ 2 weeks {'✅' if notifications['day_14'] else '❌'}",
                    callback_data="edit_notif_14",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"1️⃣ 1 month {'✅' if notifications['day_30'] else '❌'}",
                    callback_data="edit_notif_30",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"3️⃣ 3 months {'✅' if notifications['day_90'] else '❌'}",
                    callback_data="edit_notif_90",
                )
            ],
        ]
    )

    await message.answer(
        "Choose setting you want to change", reply_markup=edit_notifications_keyboard
    )


@router.callback_query(F.data.startswith("edit_notif_"))
async def handle_notification_toggle(callback: CallbackQuery):
    period = callback.data.split("_")[-1]
    client = BackendClient(callback.from_user.id)

    notifications = await client.get_notification()

    current_value = notifications.get(f"day_{period}", False)
    new_value = not current_value
    notifications[f"day_{period}"] = new_value

    await client.update_notification(
        day_0=notifications["day_0"],
        day_1=notifications["day_1"],
        day_3=notifications["day_3"],
        day_7=notifications["day_7"],
        day_14=notifications["day_14"],
        day_30=notifications["day_30"],
        day_90=notifications["day_90"],
    )

    updated_notifications = await client.get_notification()

    edit_notifications_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🕛 Day of birthday {'✅' if updated_notifications['day_0'] else '❌'}",
                    callback_data="edit_notif_0",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"1️⃣ 1 day {'✅' if updated_notifications['day_1'] else '❌'}",
                    callback_data="edit_notif_1",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"3️⃣ 3 days {'✅' if updated_notifications['day_3'] else '❌'}",
                    callback_data="edit_notif_3",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"7️⃣ 7 days {'✅' if updated_notifications['day_7'] else '❌'}",
                    callback_data="edit_notif_7",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"2️⃣ 2 days {'✅' if updated_notifications['day_14'] else '❌'}",
                    callback_data="edit_notif_14",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"1️⃣ 1 month {'✅' if updated_notifications['day_30'] else '❌'}",
                    callback_data="edit_notif_30",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"3️⃣ 3 months {'✅' if updated_notifications['day_90'] else '❌'}",
                    callback_data="edit_notif_90",
                )
            ],
        ]
    )

    await callback.message.edit_reply_markup(reply_markup=edit_notifications_keyboard)

    # Показываем всплывающее уведомление
    status = "enabled" if new_value else "disabled"
    period_name = {
        "0": "day of birthday",
        "1": "1 day",
        "3": "3 days",
        "7": "7 days",
        "14": "2 weeks",
        "30": "1 month",
        "90": "3 months",
    }.get(period, period)

    await callback.answer(f"Notifications for {period_name} {status}")
