from aiogram import types
from loaders import dp
from database.db import BotDB


@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    bot = BotDB()
    if not bot.user_exists(message.from_user.id):
        bot.add_user(message.from_user.id)
        bot.replace_curr_learned_words("", message.from_user.id)
        bot.replace_alre_learned_words("", message.from_user.id)

    await message.bot.send_message(message.from_user.id, "Hello!")
