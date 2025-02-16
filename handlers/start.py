import asyncio
from aiogram import types
import time
from aiogram.filters.command import Command
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from aiogram import F
from aiogram import Router
from aiogram import Bot
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.types import ContentType
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import CallbackQuery
from aiogram.filters.callback_data import CallbackData
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.get_chat import GetChat

import config as cfg
from markups import admin as adm
from markups import languages as langs
from aiogram.methods import GetChatMember
import states as st

import db


router = Router()  # [1]

bot = Bot(token=cfg.TOKEN)

from aiogram.filters import BaseFilter

class MyCallback(BaseFilter):
    def __init__(self, cd: str):
        self.cd = cd  # В этом фильтре мы будем ожидать, что cd — это строка

    async def __call__(self, query: types.CallbackQuery) -> bool:
        return query.data == self.cd  # Проверяем, что callback_data равно ожидаемой строке



    

#Start
@router.message(Command("start"))  # [2]
async def cmd_start(message: types.Message):
    uid = message.from_user.id
    status = 'start'
    
    if not db.check_user(uid):
        await message.answer(text="<b>Choose Language / Выберите язык</b>", reply_markup=langs.choose(), parse_mode='HTML')
        db.add_user(uid)
        db.set_status(uid, status)
    else:
        status = 'menu'
        db.upd_status(uid, status)
        lang = db.get_lang(uid)
        if lang == 'eng':
            await message.answer(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!</b>", reply_markup=langs.eng_menu(), parse_mode='HTML')
        elif lang == 'ru':
            await message.answer(text=f'<b>Доброго времени суток!</b>', reply_markup=langs.ru_menu(), parse_mode='HTML')
    
@router.callback_query(F.data == 'get_channels')
async def set_ru(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'menu'
    lang = 'ru'
    db.set_lang(uid, lang)
    db.upd_status(uid, status)
    channel = db.get_channel_cid(uid)
    lis = len(channel)
    if lis == 0:
        await callback.message.edit_text(text=f'<b>Нету привязанных каналов</b>', reply_markup=langs.add(), parse_mode='HTML')
    elif lis == 1:
        if lang == 'eng':
            await callback.message.edit_text(text=f"<b>ENG text</b>", reply_markup=langs.eng_back(), parse_mode='HTML')
        elif lang == 'ru':
            cid = channel[0]
            kb = InlineKeyboardBuilder()
            kb.row(InlineKeyboardButton(text='Channel 1', callback_data=f'{cid}'))
            await callback.message.edit_text(text=f'<b>Каналы:</b>', reply_markup=kb.as_markup(), parse_mode='HTML')
    elif lis == 2:
        if lang == 'eng':
            await callback.message.edit_text(text=f"<b>ENG text</b>", reply_markup=langs.eng_back(), parse_mode='HTML')
        elif lang == 'ru':
            cid = channel[0]
            cid1 = channel[1]
            chan = str(*cid)
            chan1 = str(*cid1)
            #print(str(*cid))
            #print(str(*cid1))

            ChatFullInfo = await bot.get_chat(chat_id=str(*cid))
            ChatFullInfo1 = await bot.get_chat(chat_id=str(*cid1))
            
            #print(ChatFullInfo.title)
            #print(ChatFullInfo1.title)

            kb = InlineKeyboardBuilder()
            kb.row(InlineKeyboardButton(text=f'{ChatFullInfo.title}', callback_data=f'channel:{chan}'))
            kb.row(InlineKeyboardButton(text=f'{ChatFullInfo1.title}', callback_data=f'channel:{chan1}'))
            await callback.message.edit_text(text=f'<b>Каналы:</b>', reply_markup=kb.as_markup(), parse_mode='HTML')
       
    
@router.callback_query(F.data.startswith('channel:'))
async def handle_channel(callback: types.CallbackQuery):
    action = callback.data
    channel_id = action.split(":")[1]
    channel_full_info = await bot.get_chat(chat_id=channel_id)
    name = channel_full_info.title
    username = channel_full_info.username
    members = await bot.get_chat_member_count(chat_id=channel_id)
    await callback.message.edit_text(f"Вы выбрали канал с ID: {channel_id}\nНазвание: {name}\nЮзернейм: {username}\nКол-во участников: {members}", reply_markup=langs.ru_back())
    # Также можно добавить дополнительную логику для работы с этим каналом
    
    
    
    
    
    


@router.callback_query(F.data == 'ru')
async def set_ru(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'menu'
    lang = 'ru'
    db.set_lang(uid, lang)
    db.upd_status(uid, status)
    lang = db.get_lang(uid)
    try:
        await bot.send_message(chat_id=6892418024, text=f'<a href="tg://openmessage?user_id={uid}">Новый пользователь!</a>\nID: @{uid}\nЯзык: Английский', parse_mode='HTML')
    except:
        pass
    if lang == 'eng':
        await callback.message.edit_text(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!</b>", reply_markup=langs.eng_menu(), parse_mode='HTML')
    elif lang == 'ru':
        await callback.message.edit_text(text=f'<b>Доброго времени суток! Я - ваш личный помощник в сфере готовки, я смогу запомнить все рецепты которые вы мне пришлёте!</b>', reply_markup=langs.ru_menu(), parse_mode='HTML')

@router.callback_query(F.data == 'eng')
async def set_eng(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'menu'
    lang = 'eng'
    db.set_lang(uid, lang)
    db.upd_status(uid, status)
    lang = db.get_lang(uid)
    try:
        await bot.send_message(chat_id=6892418024, text=f'<a href="tg://openmessage?user_id={uid}">Новый пользователь!</a>\nID: @{uid}\nЯзык: Английский', parse_mode='HTML')
    except:
        pass
    if lang == 'eng':
        await callback.message.edit_text(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!</b>", reply_markup=langs.eng_menu(), parse_mode='HTML')
    elif lang == 'ru':
        await callback.message.edit_text(text=f'<b>Доброго времени суток! Я - ваш личный помощник в сфере готовки, я смогу запомнить все рецепты которые вы мне пришлёте!</b>', reply_markup=langs.ru_menu(), parse_mode='HTML')


@router.callback_query(F.data == 'get_stat')
async def get_stat(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'get_stat'
    lang = db.get_lang(uid)
    db.upd_status(uid, status)
    stat = db.get_status(uid)
    if lang == 'eng':
        await callback.message.edit_text(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!</b>", reply_markup=langs.eng_back(), parse_mode='HTML')
    elif lang == 'ru':
       await callback.message.edit_text(text=f'Отлично, добавьте меня в качестве администратора вашего канала!\n\nКак только добавите - нажмите кнопку "Проверить"', reply_markup=langs.add_to_group())



@router.callback_query(F.data == 'get_check')
async def get(callback: types.CallbackQuery, state: FSMContext):
    uid = callback.from_user.id
    status = 'get'
    lang = db.get_lang(uid)
    db.upd_status(uid, status)
    stat = db.get_status(uid)
    if lang == 'eng':
        await callback.message.edit_text(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!</b>", reply_markup=langs.eng_back(), parse_mode='HTML')
    elif lang == 'ru':
        await state.set_state(st.GetID.cid)
        await callback.message.edit_text(text=f'<b>Перешлите мне любое сообщение из канала</b>', reply_markup=langs.forward(), parse_mode='HTML')

@router.message(st.GetID.cid, F.text | F.photo | F.document | F.contact)
async def send_id(message: types.Message, state: FSMContext):
    uid = message.from_user.id
    status = 'get_channel'
    db.upd_status(uid, status)
    stat = db.get_status(uid)
    if stat == 'get_channel':
        info = message.forward_from_chat
        cid = info.id
        name = info.title
        uname = info.username
        await state.clear()
        try:
            stat = await bot.get_chat_member(chat_id=f"@{uname}", user_id=cfg.BID)
            if stat.status == ChatMemberStatus.ADMINISTRATOR:
                await message.delete()
                await message.answer(text=f"Проверяю наличие прав....")
                await message.answer(text=f'Отлично! Я привязал "{name}" к вашему аккаунту в моей сети.')
                db.set_channel(uid, cid, uname)
            else:
                await message.delete()
                await message.answer(text=f"Проверяю наличие прав....")
                await message.answer(text=f'Беда... Видимо вы сделали что-то неправильно, вернитесь к началу и повторите снова, если вы вновь увидите это сообщение - обратитесь к создателю(@lewrtix)')
        except:
                await message.answer(text=f'Беда... Бот даже не в канале, вернитесь к началу и повторите снова, если вы вновь увидите это сообщение - обратитесь к создателю(@lewrtix)')
    else:
        await state.clear()


#settings
@router.callback_query(F.data == "settings")
async def send_pant(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'settings'
    db.upd_status(uid, status)
    lang = db.get_lang(uid)
    if lang == 'eng':
        await callback.message.edit_text(text=f"<b>Here you can Change bot language</b>", reply_markup=langs.change(), parse_mode='HTML')
    elif lang == 'ru':
        await callback.message.edit_text(text=f'<b>Тут вы можете изменить язык бота</b>', reply_markup=langs.change(), parse_mode='HTML')

@router.callback_query(F.data == "change_eng")
async def send_pant(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'change_eng'
    db.upd_status(uid, status)
    new_lang = 'eng'
    db.upd_lang(uid, new_lang)
    lang = db.get_lang(uid)
    if lang == 'eng':
        await callback.message.edit_text(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!\n\nYou're subscribe: Not found subscribe</b>", reply_markup=langs.eng_menu(), parse_mode='HTML')
    elif lang == 'ru':
        await callback.message.edit_text(text=f'<b>добро пожаловать в наш бот, вы можете смотреть любые фотографии бесплатно, а также оплатить доступ к закрытому каналу с фотографиями администратора\n\nВаша подписка: Не найдена</b>', reply_markup=langs.ru_menu(), parse_mode='HTML')

@router.callback_query(F.data == "change_ru")
async def send_pant(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'change_ru'
    db.upd_status(uid, status)
    new_lang = 'ru'
    db.upd_lang(uid, new_lang)
    lang = db.get_lang(uid)
    if lang == 'eng':
        await callback.message.edit_text(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!\n\nYou're subscribe: Not found subscribe</b>", reply_markup=langs.eng_menu(), parse_mode='HTML')
    elif lang == 'ru':
        await callback.message.edit_text(text=f'<b>добро пожаловать в наш бот, вы можете смотреть любые фотографии бесплатно, а также оплатить доступ к закрытому каналу с фотографиями администратора\n\nВаша подписка: Не найдена</b>', reply_markup=langs.ru_menu(), parse_mode='HTML')

#Back
@router.callback_query(F.data == "back")
async def menu(callback: types.CallbackQuery):
    uid = callback.from_user.id
    status = 'menu'
    db.upd_status(uid, status)
    lang = db.get_lang(uid)
    
    if lang == 'eng':
        await callback.message.delete()
        await callback.message.answer(text=f"<b>Welcome in our bot, you can watch any photos for free, as well as pay for access to the private channel with admin photos!</b>", reply_markup=langs.eng_menu(), parse_mode='HTML')
    elif lang == 'ru':
        await callback.message.delete()
        await callback.message.answer(text=f'<b>Добро пожаловать в наш бот, вы можете смотреть любые фотографии бесплатно, а также оплатить доступ к закрытому каналу с фотографиями администратора</b>', reply_markup=langs.ru_menu(), parse_mode='HTML')


#Admins only
@router.message(Command('a'))
async def apanel(message: types.Message):
    uid = message.from_user.id
    aid = 6892418024
    if uid == aid:
        await message.answer(text=f'<b>Приветсвую в Админ-Панели</b>', reply_markup=adm.apanel(), parse_mode='HTML')
    else:
        pass

@router.callback_query(F.data == "a_stats")
async def astat(callback: types.CallbackQuery):
    results = db.get_all()
    users = {len(results)}
    await callback.message.answer(text=f'<b>Статистика бота:\n\nВсего пользователей: {users}</b>', parse_mode='HTML')        