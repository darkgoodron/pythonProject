from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def genMarkup(text):
    markup = InlineKeyboardMarkup(row_width=2)
    for i in text:
        markup.insert(InlineKeyboardButton("{0} - {1}".format(i[0], i[1]), callback_data="text_{0}:{1}:{2}"
                                           .format(i[0], i[1], 0)))
    markup.add(InlineKeyboardButton("Закончить выбор слов", callback_data="text_-exit-"))
    return markup


async def get_markup_for_test() -> InlineKeyboardMarkup:
    curr_button = InlineKeyboardButton("Тест по изучаемым словам", callback_data="curr")
    alre_button = InlineKeyboardButton("Тест по пройденным словам", callback_data="alre")
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(curr_button, alre_button)
    return markup


async def get_test_question(list_words):
    import random
    random.shuffle(list_words)
    markup = InlineKeyboardMarkup(row_width=2)
    for word in list_words:
        button = InlineKeyboardButton(word, callback_data="test_" + word)
        markup.insert(button)
    return markup


async def get_start_keyboard():
    button = InlineKeyboardButton("Гоу", callback_data="test_")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(button)
    return markup