from Bot import Bot
from ReadWebPage import Game
from OctordleClone import Clone


def convert_guess(guess_result):
    result = []
    for guess in guess_result:
        if guess == "G":
            result.append(2)
        elif guess == "Y":
            result.append(1)
        else:
            result.append(0)
    return tuple(result)


GUESS_CONSTANT = 15



def safri_run():
    # game_complete is the variable that keeps track of the boards
    game_complete = 0

    # guess_num keeps track of the number of guess
    guess_num = 1

    # correct is all the correct words and the index of those words e.g correct = [("trace", 3]
    correct = []

    # Initialising the two class objects that control the browser and the bot logic
    game = Game()
    bot = Bot()

    """
    This first part is to save time as the first word with 
    the highest entropy will be "tares" so it saves time.
    """
    new_word = "tares"
    game.enter_guess(new_word)
    counter = 0
    result = game.return_guess_res()[counter]
    result = convert_guess(result)

    # Continues the game until the number of guesses exceeds the total guesses
    while guess_num < GUESS_CONSTANT:

        # Loops until the current guess is correct for the board
        while result != (2, 2, 2, 2, 2) and guess_num < GUESS_CONSTANT:
            counter += 1
            new_word = bot.get_next_word(new_word, result)
            game.enter_guess(new_word)
            result = game.return_guess_res()[counter]
            result = convert_guess(result)
            guess_num += 1

        game_complete += 1

        # adds the correct word into the array with the guess number for output at the end
        if new_word not in correct:
            correct.append((new_word, guess_num))

        # checks if the guesses exceeds the max and exits if this is the case
        if guess_num > GUESS_CONSTANT:
            print("LOOOOSER")
            break
        # checks if the game is complete
        if game_complete == 8:
            print("WINNER WINNER")
            print("Num of guesses: ", guess_num)
            break

        # returns the next board
        results = game.change_board()

        # checks if the board is complete
        if results[-1] != ["G", "G", "G", "G", "G"]:
            # converts the results from an array to a tuple
            temp_results = []
            for x in results:
                temp_results.append(convert_guess(x))
            results = temp_results

            # returns the guesses
            guesses = game.return_guesses()

            # Gets the next word and inputs it into the game
            new_word = bot.change_board(guesses, results)
            counter += 1
            game.enter_guess(new_word)
            result = game.return_guess_res()[counter]
            result = convert_guess(result)
            guess_num += 1
        else:
            # if the board is complete append the correct word into the array
            guesses = game.return_guesses()
            correct.append((guesses[-1], len(results)))

    # Prints the array of correct guess and the guesses for each board and the total score
    print(correct)
    score = 0
    for x, y in correct:
        score += y
    print("The bots score is: ", score)

    # Closes the browser and exits the program
    game.close_game()
    print("Closed")
    exit(0)
def clone_run():
    # game_complete is the variable that keeps track of the boards
    game_complete = 0

    # guess_num keeps track of the number of guess
    guess_num = 1

    # correct is all the correct words and the index of those words e.g correct = [("trace", 3]
    correct = []

    # Initialising the two class objects that control the browser and the bot logic
    game = Clone()
    bot = Bot()

    game.print_word()

    """
    This first part is to save time as the first word with 
    the highest entropy will be "tares" so it saves time.
    """
    new_word = "tares"
    print("Guess: ", new_word)
    game.enter_guess(new_word)
    counter = 0
    result = game.return_guess_results()[counter]

    # Continues the game until the number of guesses exceeds the total guesses
    while guess_num < GUESS_CONSTANT:

        # Loops until the current guess is correct for the board
        while result != (2, 2, 2, 2, 2) and guess_num < GUESS_CONSTANT:
            counter += 1
            new_word = bot.get_next_word(new_word, result)
            print("Guess: ", new_word)
            game.enter_guess(new_word)
            result = game.return_guess_results()[counter]
            guess_num += 1

        game_complete += 1

        # adds the correct word into the array with the guess number for output at the end
        if new_word not in correct:
            correct.append((new_word, guess_num))

        # checks if the guesses exceeds the max and exits if this is the case
        if guess_num > GUESS_CONSTANT:
            print("LOOOOSER")
            break
        # checks if the game is complete
        if game_complete == 8:
            print("WINNER WINNER")
            print("Num of guesses: ", guess_num)
            break

        # returns the next board
        results = game.change_board()

        # checks if the board is complete
        if results[-1] != (2,2,2,2,2):

            # returns the guesses
            guesses = game.return_guesses()

            # Gets the next word and inputs it into the game
            new_word = bot.change_board(guesses, results)
            print("Guess: ", new_word)
            counter += 1
            game.enter_guess(new_word)
            result = game.return_guess_results()[counter]
            guess_num += 1
        else:
            # if the board is complete append the correct word into the array
            guesses = game.return_guesses()
            correct.append((guesses[-1], len(results)))

    # Prints the array of correct guess and the guesses for each board and the total score
    print(correct)
    score = 0
    for x, y in correct:
        score += y
    print("The bots score is: ", score)

    # exits the program
    exit(0)

RUN = "CLONE"

if __name__ == '__main__':
    if RUN == "SAFRI":
        safri_run()
    elif RUN == "CLONE":
        clone_run()