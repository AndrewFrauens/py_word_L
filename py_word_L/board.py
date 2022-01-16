import random

import guess
from typing import Union, Iterable, Sequence
import random
import datetime


class Board:
    def __init__(self, valid_words: Sequence[str], max_guesses: int = 6, seed: Union[None, int] = None):
        """
        Board represents the state of the game
        :param valid_words: the list of words to use as the valid dictionary
        :param max_guesses: how many guesses to allow
        :param seed: a seed, could be used to set the game to a specific seed for vs. witb someone.
        """
        self.valid_words = valid_words
        self.seed = 0
        self.guesses = []
        self.key_word = ''
        self.max_guesses = max_guesses
        self.reset(seed)

    def reset(self, seed: Union[None, int]):
        """
        reset the board state
        :param seed: a seed for the random numbers. Used to keep a consistent word for comparing with someone
        """
        self.seed = self.get_new_seed(seed)
        self.guesses = []
        self.key_word = self.get_key_word(self.seed, self.valid_words).upper()

    @classmethod
    def get_new_seed(cls, seed: Union[None, int] = None):
        """
        creates a new seed for use in other functions
        :param seed: can be None if time should be the seed, otherwise provide an int
        :return: the resulting seed
        """
        # use time to seed if none is given
        return seed if seed is not None else random.seed(datetime.datetime.now())

    @classmethod
    def get_key_word(cls, seed: int, valid_words: Sequence[str], key: Union[None, str] = None):
        """
        generates the key word
        :param seed:  seed used for random number generation
        :param valid_words: the sequence of words that could be correct
        :param key: an override word that could be used instead of random selection. #todo: integrate this option into code
        :return: the selected key word to use
        """
        if key is None:
            random.seed(seed)
            return random.choice(valid_words)
        elif isinstance(key, str):
            return key

    def apply_guess(self, guess_str: str):
        """
        applies and validates a guess against the current board state
        :param guess_str:  the guess string to evaluate
        """
        if len(self.guesses) >= self.max_guesses:
            raise ValueError(f'Attempted to apply guess when already at maximum guesses of: {self.max_guesses}')
        next_guess = None
        try:
            next_guess = guess.Guess(guess_str, self.key_word, self.valid_words)
        except ValueError:
            return  # return early if invalid, should an error be raised?
        self.guesses.append(next_guess)

    def check_victory(self):
        """
        Decide whether the current board state represents victory for the player
        :return: bool of whether the player has won
        """
        if len(self.guesses) == 0:
            return False
        else:
            return all((guess.State.CORRECT == guess_state for guess_state in self.guesses[-1].get_states()))

    def check_game_over(self):
        """
        Decide whether the game is over
        :return: bool of whether player has won or the max_guesses have  been consumed
        """
        return len(self.guesses) == self.max_guesses or self.check_victory()

    def get_guess_words_str(self):
        """
        Generate the guess words
        :return: a block of all the guess words
        """
        return '\n'.join(g.get_word() for g in self.guesses)

    def get_guess_states_str(self):
        """
        generate the guess states (in emoji form)
        :return:  a block of the emoji form states
        """
        return '\n'.join(g.get_state_str() for g in self.guesses)

    def get_overall_guesses_str(self):
        """
        generate the emoji states next to the guess words for the states
        :return:  a block of emojis and words corresponding to the current board state
        """
        return '\n'.join(f'{g}' for g in self.guesses)
