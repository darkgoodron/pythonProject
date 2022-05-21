import sqlite3


class BotDB:

    def __init__(self):
        self.conn = sqlite3.connect("data_users.db")
        self.cursor = self.conn.cursor()

    def user_exists(self, user_id):
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id, ))
        return bool(len(result.fetchall()))

    def get_user_id(self, user_id):
        result = self.cursor.execute(
            "SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id, ))
        return result.fetchall()[0]

    def add_user(self, user_id):
        self.cursor.execute(
            "INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def get_curr_learned_words(self, user_id):
        result = self.cursor.execute(
            "SELECT curr_learned_words FROM users WHERE user_id = ?", (user_id,))
        return result.fetchall()[0][0]

    def get_alre_learned_words(self, user_id):
        result = self.cursor.execute(
                "SELECT `alre_learned_words` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchall()[0][0]

    def replace_curr_learned_words(self, word, user_id):
        sql = '''UPDATE users SET curr_learned_words = ? WHERE user_id = ?'''
        self.cursor.execute(sql, (word, user_id))
        return self.conn.commit()

    def replace_alre_learned_words(self, word, user_id):
        sql = '''UPDATE users SET alre_learned_words = ? WHERE user_id = ?'''
        self.cursor.execute(sql, (word, user_id))
        return self.conn.commit()

    def update_curr_learned_words(self, word, user_id):
        sql = '''UPDATE users SET curr_learned_words = curr_learned_words || ? WHERE user_id = ?'''
        self.cursor.execute(sql, (word, user_id))
        return self.conn.commit()

    def update_alre_learned_words(self, word, user_id):
        sql = '''UPDATE users SET alre_learned_words = alre_learned_words || ? WHERE user_id = ?'''
        self.cursor.execute(sql, (word, user_id))
        return self.conn.commit()

    def get_some_words(self, user_id, column_code) -> []:
        from random import randrange
        if column_code == "curr":
            data = self.get_curr_learned_words(user_id)
        else:
            data = self.get_alre_learned_words(user_id)
        if data is None or not data:
            return []
        data = data.strip().split(" ")
        if len(data) < 5:
            return []
        list_words = []
        for _ in range(5):
            random_index = randrange(len(data))
            list_words.append(data[random_index])
            del data[random_index]
        if column_code == "curr":
            string_to_database = ""
            for word in data:
                string_to_database += word + " "
            self.replace_curr_learned_words(string_to_database, user_id)
        return list_words

    def close(self):
        self.conn.close()
