from aiogram import types, Router, F, Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardButton, \
    InputMediaPhoto, BotCommand
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder
import asyncio
from hand import rt1

TOKEN = '7864752522:AAE3CkPYYhZUmMmT4K1cPMC-SZ2Hidjol_k'

BOT_TOKEN = TOKEN
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(rt1)

async def main():
    global Message, Bot
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=[BotCommand(command='menu', description='Главное меню')], scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, skip_updates=True)

asyncio.run(main())
