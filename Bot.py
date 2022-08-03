from scipy.stats import entropy
from collections import defaultdict
import itertools
from tqdm import tqdm
import pickle
import os

N_GUESS = 15
ALLOWED_GUESSES = "valid-wordle-words.txt"
ALLOWED_ANSWERS = "wordle-answers-alphabetical.txt"


# Loads the valid words
def get_valid_words():
    words = []
    with open(ALLOWED_GUESSES) as f:
        for w in f.readlines():
            words.append(w.strip())
    return words


# Loads the valid answers
def get_valid_answers():
    words = []
    with open(ALLOWED_ANSWERS) as f:
        for w in f.readlines():
            words.append(w.strip())
    return words


# Counts number of times a letter appears in a word
def count_letters(word, letter):
    return len([x for x in word if x.lower() == letter.lower()])


class Bot:
    def __init__(self):
        # Loads the words into the Bot
        self.possible_words_perm = get_valid_answers()
        self.possible_words = self.possible_words_perm
        self.all_words = get_valid_words()
        print("words loaded...")

        # Creates a variable for every single possible pattern that exists
        self.all_patterns = list(itertools.product([0, 1, 2], repeat=5))
        self.guess_word = ""

        # pattern_dict has every word saved and for each pattern stores the words that matches the word and pattern.
        self.pattern_dict = self.load_pickle()
        print("pickle loaded")

    def get_next_word(self, guess, result):

        possible_words = set(self.possible_words)
        self.guess_word = guess
        words = self.pattern_dict[self.guess_word][result]
        self.possible_words = possible_words.intersection(words)
        entropies = self.calc_entropies()
        return max(entropies, key=entropies.get)

    """
    Pattern_dict is a dictionary that stores every word 
    and for every possible patterns stores an array of every words that the matches that pattern

    load_pickle is the function that retrieves the pickle from files and stores them into the pattern_dict
    if the pickle file does not exist it creates a new one 
    - this can take a long time depending on the computers processing speed and therefore the need for pickling
    """

    def load_pickle(self):
        if 'pattern_dict.p' in os.listdir('.'):
            print("pickleeee")
            pattern_dict = pickle.load(open('pattern_dict.p', 'rb'))
        else:
            pattern_dict = self.dictionary_matrix(self.all_words)
            pickle.dump(pattern_dict, open('pattern_dict.p', 'wb+'))
        return pattern_dict

    # Matrix_maker is a the method that compares two words and returns a tuple of the result
    # matrix_maker("trace","tares") returns (2, 1, 1, 0, 1)
    def matrix_maker(self, word, guess):
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

    # Dictionary matrix is what creates the pattern_dict by cycling through every word
    # and then creating a pattern for every word with the first
    def dictionary_matrix(self, dictionary):
        pattern_dict = defaultdict(lambda: defaultdict(set))
        for word in tqdm(dictionary):
            for word2 in dictionary:
                pattern = self.matrix_maker(word, word2)
                pattern_dict[word][pattern].add(word2)
        return dict(pattern_dict)

    # Calculating entropies by counting the number of matches for each pattern for a word
    # and then using the entropy formula to get a value for this
    def calc_entropies(self):
        entropies = {}
        for word in self.possible_words:
            count = []
            for pattern in self.all_patterns:
                matches = set(self.pattern_dict[word][pattern]).intersection(self.possible_words)
                count.append(len(matches))
            entropies[word] = entropy(count)
        return entropies

    # Change board resets the possible words and
    # then runs through the new results for each guess to reduce the number of final words
    def change_board(self, guesses, results):
        self.possible_words = self.possible_words_perm
        compound = zip(guesses, results)
        for guess, result in compound:
            word = self.get_next_word(guess, result)
        return word