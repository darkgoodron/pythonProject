from aiogram import types
from loaders import dp


@dp.message_handler(commands='description')
async def command_description(message: types.Message):
    await message.answer('Этот бот создан для того, чтобы вы могли пополнять свой словарный'
                         ' запас благодаря тексту, который вы отправляете боту. Вы сможете '
                         'пополнить базу своих слов из этих текстов.')