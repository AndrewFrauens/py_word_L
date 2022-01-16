import all_valid_words

from board import Board
from guess import State


def main():
    desired_length = 5

    corrected_length_words = [word for word in all_valid_words.word_set if len(word) == desired_length]

    counting_stats = False
    if counting_stats:
        letters = 'abcdefghijklmnopqrstuvwxyz'
        counts = [0] * 26
        for letter in letters:
            for word in corrected_length_words:
                word = word.lower()
                if letter in word:
                    counts[ord(letter) - ord('a')] += 1

        pairings = [(count, letter) for letter, count in zip(letters, counts)]
        pairings = reversed(sorted(pairings))
        for count, letter in pairings:
            print(f'There are {count} words that have a "{letter.upper()}"')
        return

    board = Board(corrected_length_words, desired_length, seed=None)

    printable_char_replacements = (
        (str(State.UNEVALUATED), '_'),
        (str(State.CORRECT), '^'),
        (str(State.WRONG), 'X'),
        (str(State.MISPLACED), '?'))

    print("Let's play Word_L!!!")
    print('')

    while not board.check_game_over():
        # todo: add a way to show discovered letters/banned letters/etc
        next_word = input("\nWhat's your guess? ")
        try:
            board.apply_guess(next_word)
        except ValueError as e:
            print(e)
        print('')
        board_str = board.get_overall_guesses_str()
        for old, new in printable_char_replacements:
            board_str = board_str.replace(old, new)
        print(board_str)
        print()

    board_str = board.get_overall_guesses_str()
    for old, new in printable_char_replacements:
        board_str = board_str.replace(old, new)
    print(board_str)
    print('\n\n')
    print(board.get_guess_states_str())

    if board.check_victory():
        print('YOU WIN')
    else:
        print(f'YOU LOSE, word was: {board.key_word}')


if __name__ == '__main__':
    main()
