from aiogram import types
from loaders import dp
from database.db import BotDB
from text.correction import throw_trash_and_get_words
from buttons.button_creator import genMarkup
from data.static_variables import Words


@dp.message_handler(commands='text')
async def command_text(message: types.Message):
    user_id = message.from_user.id
    await Words.set_flag_true()

    text = message.text.replace('/text', '')
    await message.answer("Обработка информации...")

    trans_text = await throw_trash_and_get_words(text, user_id)

    if trans_text == "-er-":
        await message.bot.send_message(user_id, "Ошибка перевода текста")
        return
    if trans_text:
        inline = await genMarkup(trans_text)
        await message.answer("Выявлено " + str(len(trans_text)) + " новых слов(а)")
        await message.answer("Выберите слова:", reply_markup=inline)
    else:
        await message.bot.send_message(user_id, "Не выявлено ни одного нового слова")


@dp.callback_query_handler(lambda call: call.data.startswith("text_"))
async def process_callback(callback_query: types.CallbackQuery):
    if not await Words.get_flag():
        return
    callback_query.data = callback_query.data[5:]
    if callback_query.data != "-exit-":
        if callback_query.data not in await Words.get_words():
            await Words.add_word(callback_query.data)
    else:
        if not await Words.get_words():
            return
        string_to_database = ""
        for word in await Words.get_words():
            string_to_database += "{0} ".format(word)
        await callback_query.message.answer(str(len(Words.new_words)) + " новых(ое) слов(а): " +
                                            "\nдобавлены в ваш список изучаемых слов")
        bot = BotDB()
        bot.update_curr_learned_words(string_to_database, callback_query.message.chat.id)
        await Words.clear_words_list()
        await Words.set_flag_false()




