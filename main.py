import random

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def open_word_list():
    with open("word_list.txt") as f:
        words = f.read().split()
    return words

def valid_guess(word, word_list, attempt):
    if attempt == 1:
        ending = "st"
    elif attempt == 2:
        ending = "nd"
    elif attempt == 3:
        ending = "rd"
    else:
        ending = "th"
    user_attempt = str(input("Your {}{} guess: ".format(attempt, ending))).lower()
    while len(user_attempt) != 5 or user_attempt not in word_list:
        if len(user_attempt) != 5:
            user_attempt = str(input("Guess not 5 letters long, please try again: ")).lower()
        else:
            user_attempt = str(input("Guess not in word list, please try again: ")).lower()
    return user_attempt

def update_alphabet(alphabet, letter, colour):
    if letter in alphabet[0]:
        alphabet[0] = alphabet[0].replace(letter, "_")
        if colour == "green":
            if letter not in alphabet[1]:
                alphabet[1] += letter
        elif colour == "yellow":
            if letter not in alphabet[2]:
                alphabet[2] += letter
        else:
            if letter not in alphabet[3]:
                alphabet[3] += letter
    elif letter in alphabet[2] and colour == "green":
        alphabet[2] = alphabet[2].replace(letter, "")
        alphabet[1] += letter
    return alphabet

def one_guess(word, word_list, alphabet, attempt):
    guess = "" # provides simple string
    result = "" # provides colour-coded result to be printed in terminal
    user_attempt = valid_guess(word, word_list, attempt)
    if user_attempt == word:
        result = f"\033[0;92m{user_attempt}\33[0m"
        guess = user_attempt
        for letter in user_attempt:
            update_alphabet(alphabet, letter, "green")
    else:
        for letter in range(len(user_attempt)):
            if user_attempt[letter] == word[letter]:
                result += f"\033[0;92m{user_attempt[letter]}\33[0m" # BRIGHT GREEN
                guess += user_attempt[letter]
                update_alphabet(alphabet, user_attempt[letter], "green")
            elif user_attempt[letter] in word:
                result += f"\033[0;93m{user_attempt[letter]}\33[0m" # BRIGHT YELLOW
                guess += user_attempt[letter]
                update_alphabet(alphabet, user_attempt[letter], "yellow")
            else:
                result += user_attempt[letter]
                guess += user_attempt[letter]
                update_alphabet(alphabet, user_attempt[letter], "white")
    print(result) # visual aid for player
    return guess, alphabet

def correct_guess(secret_word, guess):
    return True if guess.lower() == secret_word.lower() else False

def play_game(attempts):
    print("\033[4mWelcome to Mark's Wordle game! You have {} attempts to guess "
          "the secret five-letter word\33[0m".format(attempts))
    alphabet = ["abcdefghijklmnopqrstuvwxyz", "", "", ""]
    word_list = open_word_list()
    word = random.choice(word_list)
    #print(f"Secret word is: {word} ")
    guesses_made = []
    for attempt in range(attempts):
        guess, fresh_alphabet = one_guess(word, word_list, alphabet, (attempt+1))
        guesses_made.append(str(guess))
        remaining_letters = f"\033[0;97m{fresh_alphabet[0]}\33[0m"
        greens = f"\033[0;92m{fresh_alphabet[1]}\33[0m"
        yellows = f"\033[0;93m{fresh_alphabet[2]}\33[0m"
        greys = fresh_alphabet[3]
        print(f"({remaining_letters})-({greens})-({yellows})-({greys})")  # provides coloured-alphabet
        if correct_guess(word, guess):
            print(f"Congratulations! You won on attempt {attempt+1}")
            break
        else:
            if (attempt+1) == attempts:
                print("Incorrect. Sorry, you're out of goes")
                print(f"Secret word was \033[0;97m{word}\33[0m")

play_game(6)
