from open_ai import OpenaiHandler


class Character:
    def __init__(self, openai_api_key, chat_id, conversation_id):
        self.ai = OpenaiHandler(openai_api_key)
        self.name = self.ai.get_char_name()
        self.prompt = self.ai.get_initial_prompt(self.name)
        self.memory = [
            {'role': 'system', 'content': self.prompt}
        ]
        self.chat_id = chat_id
        self.conversation_id = conversation_id
        self.id = None

    def generate_response(self, message_text: str):
        self.__add_to_memory('user', message_text)
        response = self.ai.get_completion(self.memory)
        self.__add_to_memory('assistant', response)
        return response

    def __add_to_memory(self, role: str, message_text: str):
        self.memory.append({
            'role': role, 'content': message_text
        })
        if len(self.memory) > 10:
            del self.memory[1:3]
