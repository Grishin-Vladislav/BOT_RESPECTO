from random import choice

from src.open_ai import OpenaiHandler
from src.config import SECRET_WORDS


def get_new_character(count):
    ai = OpenaiHandler(123)
    for i in range(count):
        print(f'CHARACTER{i + 1}\n{"*" * 20}')
        initial = ai.get_initial_prompt('{{CHAR_TRAITS}}',
                                        '{{SECRET_WORD}}')
        print(f'Instructions:\n{initial}\n')
        char_prompt = ai._get_character_prompt()
        print(f'Traits:\n{char_prompt}\n')
        word = choice(SECRET_WORDS)
        print(f'Secret word:\n{word}')
        print('*' * 20)
        print('\n\n')


get_new_character(int(input('How many characters to generate?\n')))
