from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def apanel() -> InlineKeyboardMarkup:
    apanel = InlineKeyboardBuilder()
    apanel.row(InlineKeyboardButton(text="Статистика", callback_data='a_stats'))
    apanel.add(InlineKeyboardButton(text="Рассылка", callback_data='spam'))
    return apanel.as_markup()

