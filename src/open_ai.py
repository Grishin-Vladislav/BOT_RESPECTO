import openai
from config import *
from random import sample, choice
import re


class OpenaiHandler:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.creation_model = {
            'model': GEN_MODEL,
            'temperature': GEN_TEMP,
            'presence_penalty': GEN_PRES_PENALTY,
            'frequency_penalty': GEN_FREQ_PENALTY,
            'max_tokens': GEN_MAX_TOKENS
        }
        self.reply_model = {
            'model': REPLY_MODEL,
            'temperature': REPLY_TEMP,
            'presence_penalty': REPLY_PRES_PENALTY,
            'frequency_penalty': REPLY_FREQ_PENALTY,
            'max_tokens': REPLY_MAX_TOKENS
        }

    def get_char_name(self) -> str:

        result_instructions = CHARACTER_INSTRUCTIONS
        for keyword in CHARACTER_INSTRUCTIONS_SAMPLES:
            if keyword in CHARACTER_INSTRUCTIONS:
                random_piece = choice(
                    CHARACTER_INSTRUCTIONS_SAMPLES[keyword])
                result_instructions = result_instructions.replace(keyword,
                                                                  random_piece)

        messages = [
            {"role": 'system', "content": result_instructions},
            {"role": "user", "content": self._get_character_prompt()}
        ]
        response = openai.ChatCompletion.create(
            model=self.creation_model['model'],
            temperature=self.creation_model['temperature'],
            presence_penalty=self.creation_model['presence_penalty'],
            frequency_penalty=self.creation_model['frequency_penalty'],
            max_tokens=self.creation_model['max_tokens'],
            messages=messages
        )
        print(result_instructions)
        print(messages[1]['content'])
        return response.choices[0].message["content"]

    def get_completion(self, messages):
        response = openai.ChatCompletion.create(
            model=self.reply_model['model'],
            temperature=self.reply_model['temperature'],
            presence_penalty=self.reply_model['presence_penalty'],
            frequency_penalty=self.reply_model['frequency_penalty'],
            max_tokens=self.reply_model['max_tokens'],
            messages=messages
        )
        return response.choices[0].message["content"]

    @staticmethod
    def _get_character_prompt() -> str:
        resulting_prompt = CHARACTER_PROMPT

        for stat_title, stat in CHARACTER_SAMPLE.items():
            shuffled_chars = '\n'.join(
                sample(stat['data'], stat['total_samples']))
            resulting_prompt = resulting_prompt.replace(stat_title,
                                                        shuffled_chars)

        return resulting_prompt

    @staticmethod
    def get_initial_prompt(char_name, secret_word) -> str:
        reg = r'{(\w+)}'
        result = INITIAL_PROMPT
        for char in re.findall(reg, INITIAL_PROMPT):
            result = result.replace('{' + char + '}',
                                    choice(
                                        CHARACTERISTICS_SAMPLE[char]))

        result = result.replace('_NAME_', char_name).replace(
            '_SECRET_WORD_',
            secret_word)

        temperament = None
        for question in sample(sorted(FEW_SHOTS), FEW_SHOTS_SAMPLES):
            if temperament is None:
                temperament = choice(sorted(FEW_SHOTS[question]))
                result += f' <{question}> ' \
                          f'[{choice(FEW_SHOTS[question][temperament])}]'

            else:
                result += f' <{question}> ' \
                          f'[{choice(FEW_SHOTS[question][temperament])}]'

        return result
