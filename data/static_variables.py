class Words:
    flag = False
    new_words = []
    column_code = ""
    test_words = []
    string_to_database = ""
    answer = ""

    # new_words_methods
    @staticmethod
    async def add_word(word):
        Words.new_words.append(word)

    @staticmethod
    async def get_words() -> []:
        return Words.new_words

    @staticmethod
    async def clear_words_list():
        Words.new_words = []

    # flag_methods
    @staticmethod
    async def set_flag_false():
        Words.flag = False

    @staticmethod
    async def set_flag_true():
        Words.flag = True

    @staticmethod
    async def get_flag() -> bool:
        return Words.flag

    # test_words_methods
    @staticmethod
    async def set_test_words(words):
        Words.test_words = words

    @staticmethod
    async def get_test_word() -> str:
        if Words.test_words:
            return Words.test_words[0]
        else:
            return ""

    @staticmethod
    async def take_first_test_word() -> str:
        result = Words.test_words[0]
        Words.test_words = Words.test_words[1:]
        return result

    @staticmethod
    async def clear_test_words_list():
        Words.test_words = []

    # column_code_methods
    @staticmethod
    async def set_column_code(code):
        Words.column_code = code

    @staticmethod
    async def get_column_code() -> str:
        return Words.column_code

    # string_to_database_methods
    @staticmethod
    async def set_string_to_database(value):
        Words.string_to_database += value

    @staticmethod
    async def get_string_to_database() -> str:
        return Words.string_to_database

    # answer_methods
    @staticmethod
    async def set_answer(value):
        Words.answer = value

    @staticmethod
    async def get_answer() -> str:
        return Words.answer
