import requests
import random
import time
from datetime import datetime
from util.drawings import draw_hangman
from util.utility import generate_id

url = "https://hangman-highscores-amif.onrender.com/scores"

#url = "http://127.0.0.1:5000/scores"

#global variables
amount_of_correct_letters = 0
amount_of_wrong_letters = 0
secret_word = ""

#prints menu and takes user choice
def print_menu_take_choice():

    print("1) Play Game", "2) Display high scores", "3) Quit", sep="\n")
    execute_menu_choice(input())

#match-case for executing user's choice
def execute_menu_choice(user_choice):

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

#### WORK IN PROGRESS ###
def show_highscores():
    print("HIGH SCORES")
    print("Best times")

    try:
        r = requests.get('https://hangman-highscores-amif.onrender.com/scores/formatted')
        r.raise_for_status()
        print(r.text)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching high scores: {e}")
        
#runs game for max 3 rounds, takes time
def run_game():

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

#formats game time & gives game won message
def game_won(time):

    minutes = time/60
    seconds = (time-minutes)
    #time_taken = (f"{minutes:.0f}m {seconds:.0f}s")
    print(f"WINNER! It took you {minutes:.0f} min & {seconds:.0f} sec to finish\n")
    
    full_format_time = datetime.strftime(datetime.utcfromtimestamp(time), '%H:%M:%S')
    
    add_to_highscore(full_format_time)

#### DONE? ###
def add_to_highscore(time):

    name = input("Please input a name for the leaderboard: ")
    while 10 > len(name) < 2:
        print("Name should be 2-10 characters.")
        name = input("Please input a name for the leaderboard: ")

    id = generate_id()

    myobj = {'id': id, 'time': time, 'name': name}
    x = requests.post(url, json = myobj)
    print(x.text)

#takes user guess & checks it's valid
def user_guess(guessed_letters):

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

#prints hangman and secret word ( _ _ _ _ _ / k i _ _ a / etc)
def print_game(secret_word, guessed_letters):

    global amount_of_wrong_letters
    draw_hangman(amount_of_wrong_letters)
    print(" ".join([c if c in guessed_letters else "_" for c in secret_word]))

#chooses secret word randomly from a list
def choose_secret_word():
        
    with open('words.txt', 'r') as file:
        word_list = file.read().split()
        file.close()
    return random.choice(word_list)

def main():
    print_menu_take_choice()

if __name__ == "__main__":
    main()