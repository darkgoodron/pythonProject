from aiogram import types
from loaders import dp
from buttons import button_creator
from data.static_variables import Words
from database.db import BotDB


@dp.message_handler(commands='test')
async def command_translate(message: types.Message):
    await Words.set_flag_true()
    markup = await button_creator.get_markup_for_test()
    await message.answer("Выберите тест:", reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data in ["curr", "alre"])
async def process_callback(callback_query: types.CallbackQuery):
    if not await Words.get_flag():
        return
    await Words.set_flag_false()
    bot = BotDB()
    test_words = bot.get_some_words(callback_query.message.chat.id, callback_query.data)
    if test_words and len(test_words) >= 5:
        await Words.set_column_code(callback_query.data)
        await Words.set_test_words(test_words)
        markup = await button_creator.get_start_keyboard()
        await callback_query.message.answer("Начать тест", reply_markup=markup)
    else:
        await callback_query.message.answer("Ваш текущий запас слов недостаточно большой, "
                                            "пополните его с помощью команды: /text")


@dp.callback_query_handler(lambda call: call.data.startswith("test_"))
async def process_callback(callback_query: types.CallbackQuery):
    callback_query.data = callback_query.data[5:]
    if callback_query.data:
        word = await Words.take_first_test_word()
        data_word = word.split(":")
        if callback_query.data == data_word[1]:
            await callback_query.message.answer("Вы ответили верно!")
            if await Words.get_column_code() == "curr":
                score = int(data_word[2]) + 1
                if score >= 3:
                    await callback_query.message.answer("Слово '" + data_word[0] + "' переходит на уровень изученных!")
                    string_to_database = "{0}:{1} ".format(data_word[0], data_word[1])
                    BotDB().update_alre_learned_words(string_to_database, callback_query.message.chat.id)
                else:
                    string_to_database = "{0}:{1}:{2} ".format(data_word[0], data_word[1], str(score))
                    BotDB().update_curr_learned_words(string_to_database, callback_query.message.chat.id)
        else:
            await callback_query.message.answer("Вы ответили не верно!\n"
                                                "Правильынй ответ: " + data_word[1])
            if await Words.get_column_code() == "curr":
                string_to_database = "{0}:{1}:{2} ".format(data_word[0], data_word[1], data_word[2])
                BotDB().update_curr_learned_words(string_to_database, callback_query.message.chat.id)

    word = await Words.get_test_word()
    if not word:
        await callback_query.message.answer("Тест окончен")
        return
    data_word = word.split(":")
    list_synonyms = await get_synonyms(data_word[0])
    list_synonyms.append(data_word[1])
    markup = await button_creator.get_test_question(list_synonyms)
    await callback_query.message.answer("Как переводится " + data_word[0] + "?", reply_markup=markup)


async def get_synonyms(word) -> []:
    import requests
    import re
    from goo_trans.translation import get_translation
    from bs4 import BeautifulSoup
    response = requests.get("https://www.thesaurus.com/browse/" + word)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    result = re.findall(r'term":"\w+"', scripts[-1].text)
    list_synonyms = []
    print(word)
    print("size result: " + str(len(result)))
    if len(result) >= 3:
        result = result[:3]
    for r in result:
        trans_word = await get_translation(r[7:-1])
        list_synonyms.append(trans_word.lower())
    return list_synonyms
