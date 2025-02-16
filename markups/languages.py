from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config as cfg

bot = cfg.BOT

def add_to_group() -> InlineKeyboardMarkup:
    add_to_group = InlineKeyboardBuilder()
    add_to_group.row(InlineKeyboardButton(text="Добавить в группу", url=f'https://telegram.me/{bot}?startchannel=setup&admin=change_info+delete_messages+restrict_members+invite_users+pin_messages+promote_members'))
    add_to_group.row(InlineKeyboardButton(text='Получить статистику', callback_data="get_check"))
    return add_to_group.as_markup()

def add() -> InlineKeyboardMarkup:
    add = InlineKeyboardBuilder()
    add.row(InlineKeyboardButton(text="Добавить в группу", url=f'https://telegram.me/{bot}?startchannel=setup&admin=change_info+delete_messages+restrict_members+invite_users+pin_messages+promote_members'))
    add.row(InlineKeyboardButton(text='Получить статистику', callback_data="get_check"))
    return add.as_markup()

def forward() -> InlineKeyboardMarkup:
    forward = InlineKeyboardBuilder()
    forward.row(InlineKeyboardButton(text='<< Отмена', callback_data="back"))
    return forward.as_markup()

def choose() -> InlineKeyboardMarkup:
    choose = InlineKeyboardBuilder()
    choose.row(InlineKeyboardButton(text="🇺🇸 English", callback_data='eng'))
    choose.row(InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru'))
    return choose.as_markup()

def change() -> InlineKeyboardMarkup:
    change = InlineKeyboardBuilder()
    change.row(InlineKeyboardButton(text="🇺🇸 English", callback_data='change_eng'))
    change.row(InlineKeyboardButton(text='🇷🇺 Русский', callback_data='change_ru'))
    change.row(InlineKeyboardButton(text='<< Menu', callback_data='back'))
    return change.as_markup()

#eng
def eng_menu() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.row(InlineKeyboardButton(text="📊 Get Channel Statistic", callback_data='get_stat'))
    menu.row(InlineKeyboardButton(text="⚙️ Settings", callback_data='settings'))
    return menu.as_markup()

def eng_back() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.row(InlineKeyboardButton(text='<< Menu', callback_data='back'))
    return menu.as_markup()

#ru
def ru_menu() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.row(InlineKeyboardButton(text="📊 Получить Статистику Канала", callback_data='get_stat'))
    menu.row(InlineKeyboardButton(text="Мои каналы", callback_data='get_channels'))
    menu.row(InlineKeyboardButton(text="⚙️ Настройки", callback_data='settings'))
    return menu.as_markup()

def ru_back() -> InlineKeyboardMarkup:
    menu = InlineKeyboardBuilder()
    menu.row(InlineKeyboardButton(text="<< Назад", callback_data='back'))
    return menu.as_markup()