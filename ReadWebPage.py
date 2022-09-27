from bs4 import BeautifulSoup
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re


# As we are solving the octordle sequence game we do not have to worry
# about the multiple different boards at once and we can focus one at a time

class Game:
    # Initialises the webdriver as well as the shared variables across the functions
    # driver is the actual browser
    # guessNum and guessResults are the number of guess thus far and the content of meaning of those guesses
    # board and boardNum correspond to the board we are currently solving
    def __init__(self):
        # URL = "https://octordle.com/daily"
        URL = "https://octordle.com/daily-sequence"
        # URL = "https://octordle.com/free-sequence"

        # Initialises the browser
        self.driver = webdriver.Safari()
        self.driver.get(URL)
        assert 'Octordle' in self.driver.title

        # Accepts the cookies on the page
        self.driver.find_element(By.CLASS_NAME, "cookie__floating__buttons__button--accept").click()

        # Initialising variable
        self.guessNum = 0
        self.guessResults = []
        self.guesses = []
        self.board_num = 1
        self.board = "board-" + str(self.board_num)

    # get_result is the function that reads the board and appends the latest guess to the results
    # returns result like ["B,B,B,G,B"]
    def get_result(self):
        # Gets the current board html
        soup = self.get_board()
        result = []

        # gets the current board row html from the board
        row1 = str(soup.find_all("div", class_="board-row")[self.guessNum])

        """
        For the html of the website "letter " is always before the indicators for whether the current
        letter is a exact match/in the word. This is why we use this to find all 5 examples of this.

        Warning this may break if the website html changes - may be broken if the browser changes
        """
        substr = "letter "
        search_res = [_.start() for _ in re.finditer(substr, row1)]

        for i in range(5):
            word = row1[search_res[i] + 7:search_res[i] + 12]
            if word == "word-":
                result.append("Y")
            elif word == "exact":
                result.append("G")
            else:
                result.append("B")
        self.guessResults.append(result)
        self.guessNum += 1

    # get_board returns an html 'soup' of the board that is currently in question
    def get_board(self):
        elem = self.driver.find_element(By.ID, self.board)
        html = self.driver.execute_script("return arguments[0].innerHTML;", elem)
        soup = BeautifulSoup(html, 'html.parser')
        soup.prettify()
        return soup

    # enter_guess adds the next guess to the game - guess has to be a five letter word
    def enter_guess(self, guess):
        elem = self.driver.find_element(By.ID, self.board)
        elem.send_keys(guess)
        self.guesses.append(guess)
        elem.send_keys(Keys.ENTER)
        self.get_result()

    # close_game finishes the game and closes the window
    def close_game(self):
        sleep(5)
        self.driver.close()

    # return_guess_res returns all the current guess results as an array e.g. [["B,B,B,G,B"],["B,Y,B,G,B"], ...]
    def return_guess_res(self):
        return self.guessResults

    # returns all the guessed words e.g. ["trace","sound", ...]
    def return_guesses(self):
        return self.guesses

    # change_board changes to the next board number along and returns all the current guess results for that board
    def change_board(self):
        # Change the board number by 1
        self.board_num += 1
        self.board = "board-" + str(self.board_num)
        self.guessResults = []

        # Goes through the new board and adds each result to the array stopping if the current guess is correct
        guessNum = self.guessNum
        self.guessNum = 0
        for i in range(guessNum):
            self.get_result()
            if self.guessResults[i] == ["G", "G", "G", "G", "G"]:
                self.guessNum = guessNum
                break
        return self.guessResults