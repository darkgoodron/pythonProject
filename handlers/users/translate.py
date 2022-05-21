from aiogram import types
from loaders import dp
from goo_trans.translation import get_translation


@dp.message_handler(commands='translate')
async def command_translate(message: types.Message):
    text = message.text.replace('/translate', '')
    print(text)
    if text is None or text == "":
        await message.bot.send_message(message.from_user.id, "Введите команду корректно!")
        return
    translation = await get_translation(text)
    if translation == "-er-":
        translation = "Ошибка перевода текста"
    await message.bot.send_message(message.from_user.id, translation)
