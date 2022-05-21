from googletrans import Translator


async def get_translation(word):
    translator = Translator()
    try:
        result = translator.translate(word, src='en', dest='ru')
    except:
        return "-er-"
    return result.text
