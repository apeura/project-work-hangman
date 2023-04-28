import requests
import random
import time
from datetime import datetime
from util.drawings import draw_hangman
from util.utility import *
"""
Module that contains functions relating to running hangman game and storing and displaying highscores.
Module uses global variables for keeping count of correct and wrong letters as well as the secret word.
"""
amount_of_correct_letters = 0
amount_of_wrong_letters = 0
secret_word = ""

def print_menu_take_choice():
    """Prints main menu and takes user input, which is sent to execute_menu_choice
    """
    print("1) Play Game", "2) Display high scores", "3) Quit", sep="\n")
    execute_menu_choice(input())

def execute_menu_choice(user_choice):
    """Validates user input and runs relevant functions.
    Parameters
    ----------
    String : `user_choice`
        The input that is validated and that decides which functions are ran.
    """
    try:
        int(user_choice)
    except ValueError:
        print("Invalid value, must input a whole number")
        print_menu_take_choice()

    match int(user_choice):
        case 1:
            run_game()
            print_menu_take_choice()
        case 2:
            show_highscores()
            print_menu_take_choice()
        case 3:
            quit()
        case other:
            print("Please input a number from the menu")
            print_menu_take_choice()

def show_highscores():
    """Prints top 10 highscores to console.
    """
    print("HIGH SCORES")
    print("Best times")

    r = requests.get('https://hangman-highscores-amif.onrender.com/scores/formatted')
    r.raise_for_status()
    print(r.text)

def run_game():
    """Runs hangman game for max three rounds and takes time. 
    If the game is won runs game_won function with game time.
    """
    global secret_word, amount_of_correct_letters, amount_of_wrong_letters
    incorrect_guess_limit = 6
    rounds = 1
    start = time.time()

    while rounds < 4:

        print("     *** ROUND ", rounds, "! ***", sep="")
        secret_word = choose_secret_word()
        guessed_letters = []
        amount_of_correct_letters = 0
        amount_of_wrong_letters = 0

        while incorrect_guess_limit > amount_of_wrong_letters and amount_of_correct_letters < len(secret_word):

            # leaving inner loop when game is lost
            if amount_of_wrong_letters == incorrect_guess_limit:
               break

            print_game(secret_word, guessed_letters)
            guess = user_guess(guessed_letters)

            if guess in secret_word:
                amount_of_correct_letters += secret_word.count(guess)
            else:
                amount_of_wrong_letters += 1
            guessed_letters.append(guess)
         
        print_game(secret_word, guessed_letters)
        print()

        # quitting outer loop when game is lost or won
        if amount_of_wrong_letters == incorrect_guess_limit:
            end = time.time()
            print("loser :(\n ")
            break
        elif amount_of_correct_letters == len(secret_word) and rounds == 3:
            end = time.time()
            game_won(end-start)
            break
        
        rounds += 1

def game_won(time):
    """Tells time taken to win in minutes and seconds, sends time in 00:00:00 format to add_to_highscore
    Parameters
    ----------
    Int : `time`
        The input that is re-formatted and sent foward to add_to_highscore.
    """
    minutes = time/60
    seconds = (time-minutes)

    if minutes >= 60:
        hours = minutes//60
        minutes = minutes % 60
        print(f"WINNER! It took you {hours:.0f} hour(s) {minutes:.0f} min & {seconds:.0f} sec to finish\n")
    else:
        print(f"WINNER! It took you {minutes:.0f} min & {seconds:.0f} sec to finish\n")
    
    full_format_time = datetime.strftime(datetime.utcfromtimestamp(time), '%H:%M:%S')
    
    add_to_highscore(full_format_time)

def add_to_highscore(time):
    """Takes player name and validates it's length, sends score information to score_is_added_to_top50 validation.
    If valid score gets added via post request. If not prints a message. 
    Parameters
    ----------
    String : `time`
        The input that is sent with player name to top50 validation
    """

    name = input("Please input a name for the leaderboard: ")

    while 10 > len(name) < 2:
        print("Name should be 2-10 characters.")
        name = input("Please input a name for the leaderboard: ")

    myobj = {"time": time, "name": name}
    
    if score_is_added_to_top50(myobj) == True:
        
        x = requests.post('https://hangman-highscores-amif.onrender.com/scores', json = myobj)
        print(x.text)

        print("score saved to top 50!")
    else:
        
        print("good job, but score is not good enough for top 50!")
    

def user_guess(guessed_letters):
    """ Takes user guess and validates it (hasn't been quessed before and is a single letter).
    If guess is not valid it's asked again.
    Parameters
    ----------
    String : `guessed_letters`
        The letters the player has previously guessed. Used in new guess validation.
    Returns
    -------
        The validated letter user has guessed.
    """
    guess = input("Guess a letter: ").lower()

    while guess in guessed_letters or not guess.isalpha() or len(guess) != 1:
        if guess in guessed_letters:
            print("Guess something else please.")
        elif not guess.isalpha():
            print("Guess should be alphabethical.")
        elif len(guess) != 1:
            print("Please enter only one letter.")
        guess = input("Guess a letter: ").lower()

    return guess

def print_game(secret_word, guessed_letters):
    """ Prints game taking into account guessed letters in the secret word.
    Parameters
    ----------
    String : `secret_word`
        The word that is being guessed.
    String : `guessed_letters`
        The letters the player has previously guessed.
    """
    global amount_of_wrong_letters
    draw_hangman(amount_of_wrong_letters)
    print(" ".join([c if c in guessed_letters else "_" for c in secret_word]))

def choose_secret_word():
    """ Chooses secret word from a 
    Parameters
    ----------
    String : `secret_word`
        The word that is being guessed.
    String : `guessed_letters`
        The letters the player has previously guessed.
    """
        
    with open('words.txt', 'r') as file:
        word_list = file.read().split()
        file.close()
    return random.choice(word_list)

def main():
    print_menu_take_choice()

if __name__ == "__main__":
    main()