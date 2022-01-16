from enum import Enum
from typing import Iterable


class State(Enum):
    """
    states for tiles
    """
    UNEVALUATED = 0
    WRONG = 1
    CORRECT = 2
    MISPLACED = 3

    def __str__(self):
        """
        :return: string form of State, as emoji
        """
        if self.value == State.UNEVALUATED.value:
            return '⬛'  # black square
        elif self.value == State.WRONG.value:
            return '🟥'  # red quare
        elif self.value == State.CORRECT.value:
            return '🟩'  # green square
        elif self.value == State.MISPLACED.value:
            return '🟨'  # yellow square
        else:
            raise ValueError(f'Invalid State: {State}')


class Guess:
    def __init__(self, guess: str, key: str, valid_words: Iterable[str]):
        """
        create a Guess if possible. raise a ValueError if invalid.
        :param guess: the guess string to generate a Guess from
        :param key: the key string that represents the correct value
        :param valid_words: the list of words that are legal to attempt
        """
        guess = guess.upper()
        if len(guess) != len(key):
            raise ValueError(f'Guess length does not match key length')
        if guess == key:
            self.word = guess
            self.states = [State.CORRECT] * len(guess)
        else:
            if guess not in valid_words:
                raise ValueError(f'Guess is not in the set of valid words')

            self.word = guess
            # todo: figure out a way to account for the NUMBER of misplaced letters?
            self.states = [
                State.CORRECT if guess_letter == key_letter
                else State.MISPLACED if guess_letter in key
                else State.WRONG
                for
                guess_letter, key_letter in zip(guess, key)]

    def get_state_str(self):
        """
        :return: get the emoji string for the current states of the guess
        """
        return ''.join(map(str, self.states))

    def get_states(self):
        """
        :return: get the list of enums for the states of the guess tiles
        """
        return self.states

    def spoiler_free_str(self):
        """
        :return: get the states of the tiles without the letters to avoid spoilers
        """
        return self.get_state_str()

    def get_word(self):
        """
        :return: get the word that this Guess represents as a string
        """
        return self.word

    def __str__(self):
        """
        :return: get the string form of a guess
        """
        return f'{self.get_word()} {self.get_state_str()}'
