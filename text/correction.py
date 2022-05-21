import re
from database.db import BotDB
from goo_trans.translation import get_translation


async def correct_text(text):
    text = re.sub(r"\n+", " ", text)
    text = re.sub(r"https\S+", "", text)
    text_list = re.sub(r"[^a-zA-Z ]+", "", text).split(' ')
    text_list = [elem for elem in text_list if elem.strip()]
    text_list = [t.lower() for t in text_list]
    text_list = list(dict.fromkeys(text_list))
    return text_list


async def throw_trash_and_get_words(text, user_id):
    translation_list = []
    data_list = await get_data_list(user_id)
    text_list = await correct_text(text)
    for word in text_list:
        if word in data_list:
            continue
        trans_word = await get_translation(word)
        if trans_word == "-er-":
            return "-er-"
        trans_word = trans_word.lower()
        if trans_word == word:
            continue
        translation_list.append((word, trans_word))
    return translation_list


async def get_data_list(user_id):
    bot = BotDB()
    curr_data = bot.get_curr_learned_words(user_id)
    if curr_data is None or curr_data == "":
        return ""
    else:
        result = []
        for data in curr_data.strip().split(' '):
            data_split = data.split(":")
            result.append(data_split[0])
        return result

