import logging
from aiogram import Bot, Dispatcher, executor, types
import os
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)

bot_token = os.getenv("API_TOKEN")

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())

saved_data = {}


class Form(StatesGroup):
    name = State()
    cash = State()


class Form2(StatesGroup):
    name2 = State()
    sum = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я самый умный telegram-бот от Вики и Даши!")

@dp.message_handler(commands=['save_currency'])
async def start_command(message: types.Message):
    await Form.name.set()
    await message.reply('Введите название валюты')


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    print(message.text)
    await state.update_data(name=message.text)
    user_data = await state.get_data()
    await Form.cash.set()
    await message.reply("Курс валюты к рублю")


@dp.message_handler(state=Form.cash)
async def process_cash(message: types.Message, state: FSMContext):
    print(message.text)
    await state.update_data(cash=message.text)
    user_data = await state.get_data()
    saved_data['form1'] = user_data
    await state.finish()
    await message.reply("Курс валюты сохранен")


@dp.message_handler(commands=['convert'])
async def start_command2(message: types.Message):
    await Form2.name2.set()
    await message.reply('Введите название валюты')


@dp.message_handler(state=Form2.name2)
async def process_name2(message: types.Message, state: FSMContext):
    await state.update_data(name2=message.text)
    user_data2 = await state.get_data()
    await Form2.sum.set()
    await message.reply("Колическтво валюты")


@dp.message_handler(state=Form2.sum)
async def process_sum(message: types.Message, state: FSMContext):
    await state.update_data(sum=message.text)
    user_data2 = await state.get_data()
    print(saved_data)
    print(user_data2)
    await message.reply(int(user_data2['sum']) / int(saved_data['form1']['cash']))


if __name__ == "__main__":
    dp.middleware.setup(LoggingMiddleware())
    executor.start_polling(dp, skip_updates=True)

#if (user_data[name] == user_data[name2]):
