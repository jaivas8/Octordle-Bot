import random

ALLOWED_ANSWERS = "wordle-answers-alphabetical.txt"


def get_valid_answers():
    words = []
    with open(ALLOWED_ANSWERS) as f:
        for w in f.readlines():
            words.append(w.strip())
    return words


def count_letters(word, letter):
    return len([x for x in word if x.lower() == letter.lower()])


def matrix_maker(word, guess):
    matrix = [0, 0, 0, 0, 0]
    good_letters = {}
    for letter in word:
        good_letters[letter] = count_letters(guess, letter)
    for i in range(0, 5):
        if word[i] == guess[i]:
            matrix[i] = 2
            good_letters[word[i]] -= 1
    for i in range(0, 5):
        if word[i] in guess and matrix[i] != 2:
            if word[i] in good_letters.keys() and good_letters[word[i]] > 0:
                matrix[i] = 1
                good_letters[word[i]] -= 1
    return tuple(matrix)


class Clone:
    def __init__(self):
        valid_words = get_valid_answers()
        self.final_words = random.sample(valid_words, 8)
        self.current_word = 0
        self.guesses = []
        self.guessNum = 0
        self.guessResults = []

    def enter_guess(self,guess):
        self.guesses.append(guess)
        self.get_result()

    def get_result(self):
        result = matrix_maker(self.guesses[self.guessNum], self.final_words[self.current_word])
        self.guessNum += 1
        self.guessResults.append(result)

    def return_guess_results(self):
        return self.guessResults

    def return_guesses(self):
        return self.guesses

    def change_board(self):
        self.current_word += 1
        self.guessResults = []

        guessNum = self.guessNum
        self.guessNum = 0
        for i in range(guessNum):
            self.get_result()
            if self.guessResults[i] == ["G", "G", "G", "G", "G"]:
                self.guessNum = guessNum
                break

        return self.guessResults

    def print_word(self):
        print(self.final_words)


