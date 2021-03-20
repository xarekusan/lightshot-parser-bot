import logging

from shutil import rmtree
from os import remove
from aiogram import Bot, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, \
                        KeyboardButton
from this_is_script import start_script
from settings import (BOT_TOKEN)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

btn_parsing = KeyboardButton("/parsing")
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_parsing)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет!\nНажми на кнопку ниже, чтобы начать парсинг",
                           reply_markup=greet_kb)


@dp.message_handler(commands=["parsing"])
async def parsing(message: types.Message):
    filename = start_script()
    with open(filename, 'rb') as photo:
        try:
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        except Exception:
            await bot.send_message(chat_id=message.chat.id, text="Error. Try again")
    remove(filename)
    rmtree('.cache', ignore_errors=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
