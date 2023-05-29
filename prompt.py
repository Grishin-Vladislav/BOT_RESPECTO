import os
import openai
from config import *
from dotenv import load_dotenv, find_dotenv
from random import sample
from random import choice
import re

load_dotenv(find_dotenv())


class PromptFactory:
    openai.api_key = os.getenv('OPENAI_API_KEY')
    model = model
    temperature = temperature
    presence_penalty = presence_penalty
    frequency_penalty = frequency_penalty
    max_tokens = max_tokens

    @classmethod
    def get_char_name(cls) -> str:
        messages = [
            {"role": 'system', "content": character_instructions},
            {"role": "user", "content": cls.get_character_prompt()}
        ]
        response = openai.ChatCompletion.create(
            model=cls.model,
            temperature=cls.temperature,
            presence_penalty=cls.presence_penalty,
            frequency_penalty=cls.frequency_penalty,
            max_tokens=cls.max_tokens,
            messages=messages
        )
        print(character_instructions)
        print(messages[1]['content'])
        return response.choices[0].message["content"]

    @staticmethod
    def get_character_prompt() -> str:
        shuffled_chars = ' '.join(
            sample(character_sample, number_of_samples))
        return character_prompt.replace('_SAMPLE_', shuffled_chars)

    @classmethod
    def get_initial_prompt(cls, char_name) -> str:
        reg = r'{(\w+)}'
        result = initial_prompt
        for char in re.findall(reg, initial_prompt):
            result = result.replace('{' + char + '}',
                                    choice(characteristics_sample[char]))
        return result.replace('_NAME_', char_name)

    @classmethod
    def get_completion(cls, messages):
        response = openai.ChatCompletion.create(
            model=cls.model,
            temperature=cls.temperature,
            presence_penalty=cls.presence_penalty,
            frequency_penalty=cls.frequency_penalty,
            max_tokens=cls.max_tokens,
            messages=messages
        )
        return response.choices[0].message["content"]
