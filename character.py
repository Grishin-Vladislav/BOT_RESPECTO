from prompt import PromptFactory as pf


class Character:

    def __init__(self):
        self.name = pf.get_char_name()
        self.prompt = pf.get_initial_prompt(self.name)
        self.memory = [
            {'role': 'system', 'content': self.prompt}
        ]

    def __add_to_memory(self, role: str, message_text: str):
        self.memory.append({
            'role': role, 'content': message_text
        })

    def generate_response(self, message_text: str):
        self.__add_to_memory('user', message_text)
        response = pf.get_completion(self.memory)
        self.__add_to_memory('assistant', response)
        return response
