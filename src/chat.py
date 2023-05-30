from character import Character
from config import WIN_TRIGGERS, LOSE_TRIGGERS


class ChatHandler:
    def __init__(self, api_key):
        self.openai_api_key = api_key
        self.chats = {}

    def add_conversation(self, chat_id):
        if self._is_chat_exists(chat_id):
            return
        self.chats[chat_id] = Character(self.openai_api_key)

    def remove_conversation(self, chat_id):
        del self.chats[chat_id]

    def get_character(self, chat_id):
        if self._is_chat_exists(chat_id):
            return self.chats[chat_id]

    @staticmethod
    def is_user_win(message):
        return any(trigger in message.lower() for trigger in WIN_TRIGGERS)

    @staticmethod
    def is_user_lost(message):
        return any(trigger in message.lower() for trigger in LOSE_TRIGGERS)

    def _is_chat_exists(self, chat_id):
        return chat_id in self.chats
