import requests
import random
import time
from util.drawings import draw_hangman

<<<<<<< HEAD
=======
app = Flask(__name__)
#Url /score?
<<<<<<< HEAD
url = 'http://127.0.0.1:5000/score'
=======
url = 'https://127.0.0.1/scores'
>>>>>>> d1e55c5ea47cc9e469ccea162ee84d06f90d5beb

>>>>>>> a346125e6cc47ea586dc325ec799cfc0ac3254ee
#global variables, näkyy kaikille funktioille
amount_of_correct_letters = 0
amount_of_wrong_letters = 0
secret_word = ""

#printtaa menun ja ottaa user inputin, input lähetetään execute_menu_choice funktioon
def print_menu_take_choice():

    print("1) Play Game", "2) Display high scores", "3) Quit", sep="\n")
    execute_menu_choice(input())

#match-case johon käyttähän antama int menee, käynnistää eri funktioita sen perusteella minkä numeron käyttäjä on antanut
def execute_menu_choice(user_choice):

    try:
        int(user_choice)
    except ValueError:
        print("Invalid value, must input a whole number")
        print_menu_take_choice()

    match int(user_choice):
        #käynnistää pelin, once over vie alkuun
        case 1:
            run_game()
            print_menu_take_choice()
        #näyttää highscoret, once done vie alkuun
        case 2:
            show_highscores()
            print_menu_take_choice()
        #Quit, lopettaa apin
        case 3:
            quit()
        #Jos joku muu kuin yllä annettu int: printtaa viestin ja vie alkuun
        case other:
            print("Please input a number from the menu")
            print_menu_take_choice()

#KESKEN
def show_highscores():
    print("HIGH SCORES")

#Pelin käynnistys, kaksi while looppia jotka menee kunnes voitto/häviö. Voitosta mennään voitto funktioon, häviöstä häviöön.
def run_game():
    #incorrect_guess_limittiä käytetään pelin lopettamisessa, start aloittaa ajan ottamisen
    global secret_word, amount_of_correct_letters, amount_of_wrong_letters
    incorrect_guess_limit = 6
    rounds = 1
    start = time.time()

    #ulommainen loop: jatkuu kun roundeja on vähemmän kuin 4
    #ottaa arvuutettavan sanan choose_secret_word funktion kautta 
    #nollaa muuttujat uuden roundin kohdalla + uus secret word
    while rounds < 4:

        print("     *** ROUND ", rounds, "! ***", sep="")
        secret_word = choose_secret_word()
        guessed_letters = []
        amount_of_correct_letters = 0
        amount_of_wrong_letters = 0

        #sisempi loop: jatkuu kun vääriä arvauksia on vähemmän kuin 6 ja kun oikeita on vähemmän kuin secret wordin (arvuutettavan sanan) pituus
        while incorrect_guess_limit > amount_of_wrong_letters and amount_of_correct_letters < len(secret_word):

            # sisemmästä loopista lähteminen kun tulee häviö
            if amount_of_wrong_letters == incorrect_guess_limit:
               game_lost()
               break

            # pelin printtaus, välitetään secret word ja guessed letters 
            # pelaajan arvaus otetaan user_guess funktiolla, välitetään guessed letters (jotta ei arvaa samaa)
            print_game(secret_word, guessed_letters)
            guess = user_guess(guessed_letters)

            #jos arvattu kirjain on secret wordissä --> correct letters amounttiin lisätään oikein menneiden kirjainten lkm
            #jos ei --> kasvatetaan wrong lettersin amounttia
            #lisätään arvattu kirjain guessed lettersiin
            if guess in secret_word:
                amount_of_correct_letters += secret_word.count(guess)
            else:
                amount_of_wrong_letters += 1
            guessed_letters.append(guess)
         
        print_game(secret_word, guessed_letters)
        print()

        # ulomman loopin pysäyttäminen jos on häviö/voitto, timerien lopetus
        if amount_of_wrong_letters == incorrect_guess_limit:
            end = time.time()
            game_lost()
            break
        elif amount_of_correct_letters == len(secret_word) and rounds == 3:
            end = time.time()
            game_won(end-start)
            break
        #Roundsien lisääminen
        rounds += 1

#jos voitti niin kerrotaan aika, minuuteissa jos yli 60 sec, jos alle niin sekunneissa
#!!! Kesken, pitää vielä ottaa ylös highscoret !!!!
def game_won(time):

    minutes = time/60
    seconds = (time-minutes)

    print(f"WINNER! It took you {minutes:.0f} min & {seconds:.0f} sec to finish\n")

                #time jaetaan 60 jos yli 1 min
    time_taken = time / 60 if time > 60.0 else time
                #jos yli 60 sec unit = minuutti else sekuntti
    unit = "minutes" if time > 60.0 else "seconds"
    print(f"WINNER! It took you {time_taken:.5f} {unit} to finish\n")

    add_to_highscore(time_taken)

def add_to_highscore(time):

    name = input("Please input a name for the leaderboard: ")
    while 10 > len(name) < 2:
        print("Name should be 2-10 characters.")
        name = input("Please input a name for the leaderboard: ")

    myobj = {'time': time, 'name': name}
    x = requests.post(url, json = myobj)
    print(x.text)

#loser :(
def game_lost():
    print("loser :(\n ")

#otetaan pelaajan arvaus, jos invalid arvaus pyydetään antaan uus
def user_guess(guessed_letters):

    guess = input("Guess a letter: ").lower()
    #kun arvaus on arvatuissa kirjaimissa tai kun arvaus ei ole aakkosissa tai jos pituus ei ole 1
    while guess in guessed_letters or not guess.isalpha() or len(guess) != 1:
        #jos arvaus on arvatuissa kirjaimissa
        if guess in guessed_letters:
            print("Guess something else please.")
        elif not guess.isalpha():
            print("Guess should be alphabethical.")
        #jos arvausksen pituus ei ole 1 
        elif len(guess) != 1:
            print("Please enter only one letter.")
        guess = input("Guess a letter: ").lower()

    return guess

#printtaa pelin, draw_hangman sisältää ascii hangmanit 
# printtaa _ _ _ _ _ / k _ o i r _ / etc riippuen arvatuista kirjaimista 
def print_game(secret_word, guessed_letters):

    global amount_of_wrong_letters
    draw_hangman(amount_of_wrong_letters)
    print(" ".join([c if c in guessed_letters else "_" for c in secret_word]))

#otetaan randomilla secret word text filesta luodusta listasta
def choose_secret_word():
        
    with open('words.txt', 'r') as file:
        word_list = file.read().split()
        file.close()
    return random.choice(word_list)

#aloitetaan peli
def main():
    print_menu_take_choice()


#validointi, testaus