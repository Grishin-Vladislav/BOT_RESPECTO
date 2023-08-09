from unittest.mock import patch, MagicMock
import re

import pytest

from src.open_ai import OpenaiHandler
from src.config import CHARACTER_SAMPLE, CHARACTER_PROMPT


def fake_sample(population, k):
    return population[:k]


@pytest.fixture(scope='session')
def open_ai_handler():
    return OpenaiHandler(api_key=123)


@patch('src.open_ai.sample', side_effect=fake_sample)
def test_get_character_prompt(mocked_sample, open_ai_handler):
    expected_line = CHARACTER_PROMPT
    regex = r'(_[a-zA-Z0-9]+_)'
    for match in re.findall(regex, CHARACTER_PROMPT):
        expected_line = expected_line.replace(match,
                                              CHARACTER_SAMPLE[match]['data'][0])

    sample_result = mocked_sample([1, 2, 3, 4, 5], 3)
    assert sample_result == [1, 2, 3], 'fake sample broken'
    assert open_ai_handler._get_character_prompt() == expected_line, 'unexpected result in population'


def test_get_initial_prompt(open_ai_handler):
    assert 1 + 1 == 2


def test_get_character_instructions(open_ai_handler):
    assert 1 + 1 == 2
