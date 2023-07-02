from character import Character
from config import LOSE_TRIGGERS, ANTI_LOSE_TRIGGERS


class ConversationHandler:
    def __init__(self, api_key):
        self.openai_api_key = api_key
        self.chars = {}

    def create_character(self, chat_id, conversation_id):
        self.chars[chat_id] = Character(self.openai_api_key, chat_id,
                                        conversation_id)
        return self.chars[chat_id]

    def remove_character(self, chat_id):
        del self.chars[chat_id]

    def get_character(self, chat_id):
        if self.is_character_exists(chat_id):
            return self.chars[chat_id]

    @staticmethod
    def is_user_win(message, character: Character):
        return character.secret_word in message.lower()

    @staticmethod
    def is_user_lost(message):
        triggered_lose = any(
            trigger in message.lower() for trigger in LOSE_TRIGGERS)
        triggered_anti_lose = any(
            trigger in message.lower() for trigger in ANTI_LOSE_TRIGGERS)

        return triggered_lose and not triggered_anti_lose

    def is_character_exists(self, chat_id):
        return chat_id in self.chars
