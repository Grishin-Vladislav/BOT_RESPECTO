from open_ai import OpenaiHandler
from random import choice

from config import SECRET_WORDS, USER_WRAP, BOT_WRAP


class Character:
    def __init__(self, openai_api_key, chat_id, conversation_id):
        self.ai = OpenaiHandler(openai_api_key)
        self.name = self.ai.get_char_name()
        self.secret_word = self.__get_secret_word()
        self.prompt = self.ai.get_initial_prompt(self.name,
                                                 self.secret_word)
        self.memory = [
            {'role': 'system', 'content': self.prompt}
        ]
        self.chat_id = chat_id
        self.conversation_id = conversation_id
        self.id = None

    def generate_response(self, message_text: str):
        half = len(USER_WRAP) // 2
        tag1, tag2 = USER_WRAP[:half], USER_WRAP[half:]

        self.__add_to_memory('user', f'{tag1}{message_text}{tag2}')
        response = self.ai.get_completion(self.memory)
        self.__add_to_memory('assistant', response)
        return response.strip(f"{BOT_WRAP}")

    def __add_to_memory(self, role: str, message_text: str):
        self.memory.append({
            'role': role, 'content': message_text
        })
        if len(self.memory) > 6:
            del self.memory[1:3]

    @staticmethod
    def __get_secret_word():
        return choice(SECRET_WORDS)
