# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 17:28:20 2020

@author: petrs
"""

import random
import string
import cProfile

def game():
    # we initialise main parameters of the game
    language, player1, player2, difficulty1, difficulty2, attempts, rounds = get_parameters()
    # language, player1, player2, difficulty1, difficulty2, attempts, rounds = "c", "c", "c", 1, 4, 4, 100
    wordlist, lettersAvailable = loadWords(language)
    victories = [0,0,0]
    if difficulty1 == 2 or difficulty2 == 2:
        frequency_dict = get_frequency_dictionary(wordlist)
    else:
        frequency_dict = None
    if difficulty1 == 3 or difficulty2 == 3:
        DB_len_dicts = get_DB_len_dicts(wordlist)
        # print(DB_len_dicts)
        DB_freq_dicts = get_DB_freq_dicts(DB_len_dicts, language)
        # print(DB_freq_dicts)
    else:
        DB_freq_dicts = None
    # we start a round of game. Have a loop to track number of rounds
    # print (DB_freq_dicts)
    for i in range(rounds):
        winner = hangman(player1, player2, difficulty1, difficulty2, attempts, wordlist, frequency_dict, DB_freq_dicts, lettersAvailable[:], language)
        if winner == 1:
            victories[0] += 1
        elif winner == 2:
            victories[1] += 1
        else:
            victories[2] += 1
    print(victories)
    return 0

# function to define main parameters of the game
def get_parameters():
    language = get_select_language()
    player1 = get_select_player(1)
    difficulty1 = get_select_AIlevel(player1)
    player2 = get_select_player(2)
    difficulty2 = get_select_AIlevel(player2)
    attempts = get_select_attempts()
    rounds = get_select_rounds()           
    return language.lower(), player1.lower(), player2.lower(), difficulty1, difficulty2, attempts, rounds

# Function to select language
def get_select_language():
    while True:
        language = input("Please select language. \"E\" for English, \"C\" for Czech: ")
        if (language == "E" or language == "C" or language == "e" or language == "c"):
            break
        else:
            print("Incorrect input. Please try again!")
    return language

# Function to select second player
def get_select_player(i):
    while True:
        if i == 1:
            player2 = input("Please select player  1. \"H\" for human, \"C\" for computer: ")
        else:
            player2 = input("Please select player  2. \"H\" for human, \"C\" for computer: ")
        if (player2 == "H" or player2 == "C" or player2 == "h" or player2 == "c"):
            break
        else:
            print("Incorrect input. Please try again!")
    return player2

# Function to select difficulty of AI opponent
def get_select_AIlevel(player2):
    while True:
        if player2 == "H" or player2 == "h":
            difficulty = 0
            break
        else:
            difficulty = input("Please enter a difficulty. 1 for easy, 2 for medium, 3 for hard, 4 for ultra-hard: ")
            try: 
                difficulty = int(difficulty)
                if difficulty == 1 or difficulty == 2 or difficulty == 3 or difficulty == 4:
                    break
                else:
                    print("Incorrect input. Please try again!")
            except ValueError:
                print(difficulty, "is not an integer.")    
    return difficulty

# Function to select number of attempts
def get_select_attempts():
    while True:
        attempts = input("Please enter number of attempts (1-26): ")
        try: 
            attempts = int(attempts)
            if attempts > 0 and attempts < 27:
                break
            else:
                print("Incorrect input. Please try again and select between 1 and 26!")
        except ValueError:
            print(attempts, "is not an integer.")   
    return attempts

# Function to select number of rounds
def get_select_rounds():
    while True:
        rounds = input("Please enter number of rounds you want to play: ")
        try: 
            rounds = int(rounds)
            if rounds > 0:
                break
            else:
                print("Incorrect input. Please try again and number higher than 0!")
        except ValueError:
            print(rounds, "is not an integer.")  
    return rounds

# Function to load a dictionary
def loadWords(language):
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    # WORDLIST_FILENAME = "words.txt"
    WORDLIST_FILENAME = select_dictionary(language)
    inFile = open(WORDLIST_FILENAME, 'r', encoding = "utf8")
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    lettersAvailable = get_list_available_letters(language)
    return wordlist, lettersAvailable

def get_list_available_letters(language):
    if language == "e":
        return split(string.ascii_lowercase)
    if language == "c":
        return ["a", "á", "b", "c", "č", "d", "ď", "e", "é", "ě", "f", "g", "h", "ch", "i", "í", "j", "k", "l", "m", "n", "ň", "o", "ó", "p", "q", "r", "ř", "s", "š", "t", "ť", "u", "ú", "ů", "v", "w", "x", "y", "ý", "z", "ž"]

#  Function to select a dictionary based on language
def select_dictionary(language):
    if language == "e":
        return "words.txt"
    if language == "c":
        return "czech-updated.txt"

#  Function to select a random word we will be guessing
def chooseWord(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

#  Function to split word into a list of chars
def split(word): 
    return [char for char in word]

#  Function to select a secret word
def select_secret_word(wordlist):
    return random.choice(wordlist)

# Function to get a human guess
def get_human_guess(lettersAvailable, available_words):
    while True:
        print("Available words: ", available_words)
        human_guess = input("Please guess a letter: ").lower()
        print("-------------")
        if human_guess in lettersAvailable:
            return human_guess
        else:
            print(human_guess, "is not an available character!")
            print("Select one of the following available chars:", lettersAvailable)
            print("-------------")
    return human_guess

# Function to process guesses
def guess(player, difficulty, guess_left, wordlist, lettersAvailable, frequency_dict, DB_freq_dicts, len_secret_word, shortened_wordlist, letters_guessed_dict, secret_word_hint, language):
    # Difficulty == 0, human player
    if difficulty == 0:
        shortened_wordlist_human = wordlist_curation(shortened_wordlist, letters_guessed_dict, secret_word_hint, language)
        myguess = get_human_guess(lettersAvailable, len(shortened_wordlist_human))
    elif difficulty == 1:
        myguess = get_random_guess(lettersAvailable)
    elif difficulty == 2:
        myguess = get_frequency_guess(lettersAvailable, frequency_dict)
    elif difficulty == 3:
        myguess = get_frequency_guess(lettersAvailable, DB_freq_dicts[len_secret_word])
    elif difficulty == 4:
        # print("Delka slovniku PRED curation:", len(shortened_wordlist))
        shortened_wordlist = wordlist_curation(shortened_wordlist, letters_guessed_dict, secret_word_hint, language)
        # print("Delka slovniku PO curation:", len(shortened_wordlist))
        # if len(shortened_wordlist) < 100:            
        #     print("Available words: ", shortened_wordlist)
        # else:
        #     print("Available words: ", len(shortened_wordlist))
        myguess = get_frequency_guess(lettersAvailable, get_frequency_dictionary(shortened_wordlist, language))
    return myguess

def wordlist_curation(shortened_wordlist, letters_guessed_dict, secret_word_hint, language):
    # print("Aktualni klic pro slovnik: ", letters_guessed_dict)
    # print("HINT: ", secret_word_hint)
    if len(letters_guessed_dict) == 0:
        return shortened_wordlist
    else:
        temp = []
        for item in shortened_wordlist:
            priznak = True
            for key, value in letters_guessed_dict.items():
                if item.count(key) != value:
                    priznak = False
            if priznak == True:
                temp.append(item)
        temp2 = []
        for item in temp:
            if compare(item, secret_word_hint) == True:
                temp2.append(item)                
        return temp2

def compare(a, b):
    for x, y in zip(a, b):
        if x != y:
            if y != "_":
                return False
    return True

# Function to give a random guess
def get_random_guess(lettersAvailable):
    return random.choice(lettersAvailable)

# Function to give a guess based on constant frequency of words
def get_frequency_guess(lettersAvailable, frequency_dict):
    for item in frequency_dict:
        if item in lettersAvailable:
            # print("Computer chooses ", item)
            return item

# Function to announce number of guesses left and available letters
def vyzva_selection(player1, player2, player1_turn, guess_left, lettersAvailable):
    if player1 == "c" and player2 == "c":
        return
    else:
        announce_start(player1_turn)
        print("You have ", guess_left, " guesses left.")
        print("Available letters:", lettersAvailable)
        print("-------------")
        return

# Function to announce starting player:
def announce_start(player1_turn):
    if player1_turn == True:
        print("-------------")
        print("Player 1 plays.")
        print("-------------")
    else:
        print("-------------")
        print("Player 2 plays.")
        print("-------------")

# Function to give us hint about secret word
def secret_word_hint(letters_guessed, secret_word_list, player1, player2):
    hint = []
    for item in secret_word_list:
        if item in letters_guessed:
            hint.append(item)
        else:
            hint.append("_")
    hint_string = ''.join(hint)
    if player1 == "c" and player2 == "c":
        return hint_string
    else:
        print("Your are guessing a word", len(secret_word_list),"words long: ", hint_string, end="")
        print("\n")
        return hint_string
    # else:
    #     print("Your are guessing a word", len(secret_word_list),"words long: ", end="")
    #     for item in secret_word_list:
    #         if item in letters_guessed:
    #             print(item, end="")
    #         else:
    #             print(" _ ", end="")
    #     print("\n")

# Function to check whether a letter is in the secret word:
def is_in_secretword(letter_guessed, secret_word):
    if letter_guessed in secret_word:
        # print(letter_guessed, "is in word", secret_word)
        return True
    else:
        # print(letter_guessed, "is NOT in word", secret_word)
        return False

# Function to determine turns for the next turns:
def determination_of_next_turn(player1_turn, guess_left_p1, guess_left_p2, correct_guess):
    # if a correct solution was selected, the same player has a turn and loses no available turns
    if correct_guess == True:
        return player1_turn, guess_left_p1, guess_left_p2
    # if incorrect solution was selected
    else:
        # user loses a turn
        if player1_turn == True:
            guess_left_p1 -= 1
        else:
            guess_left_p2 -= 1      
    # return updated values, by not, you switch the players
    return not player1_turn, guess_left_p1, guess_left_p2

#  Function to update the list of available letters
def update_letters_available(lettersAvailable, letter_guessed):
    # print("Vychozí seznam: ", lettersAvailable)
    # print("Guess: ", letter_guessed)
    for item in lettersAvailable:
        if item == letter_guessed:
            lettersAvailable.remove(item)
            return lettersAvailable

#  Function to check whether a word had been guessed correctly
def word_guessed (secret_word_list, letters_guessed):
    for item in secret_word_list:
        if item not in letters_guessed:
            return False
    return True

#  Function to announce victory:
def announce_victory(player1_turn, player1, player2, secret_word):
    if player1 == "c" and player2 == "c":
        return
    else:
        if player1_turn == True:
            print("Player 1 wins. ", end="")
        else:
            print("Player 2 wins. ", end="")
        print ("The correct word is", secret_word)
        print("-------------")
        print("-------------")
        print("\n")

#  Function to announce loss:
def announce_loss(player1, player2, secret_word):
    if player1 == "c" and player2 == "c":
        return
    else:
        print("No one wins. The correct word was ", secret_word)

#  Function to announce guessed word by the computer in a game against the computer
def announce_guess(player1, player2, guess, player1_turn):
    if player1 == "c" and player2 == "c":
        return
    elif player1 == "c" and player1_turn == True:
        print("The Computer guessed", guess)
    elif player2 == "c" and player1_turn == False:
        print("The Computer guessed", guess)
    return

# Function to create an empty alphanumeric dictionary
def create_empty_alpha_dict(language):
    temp_dictionary = {}
    # for item in string.ascii_lowercase:
    for item in get_list_available_letters(language):
        temp_dictionary[item] = 0
    return temp_dictionary

# function to create a frequency dictionary based on a given wordlist
def create_frequency_dict(wordlist, language):
    temp_dictionary = create_empty_alpha_dict(language)       
    for item in wordlist:
        for char in item:
            temp_dictionary[char] += 1
    return temp_dictionary

# Function to create a dictionary of most frequent characters in a wordlist
def get_frequency_dictionary(wordlist, language):
    temp_dictionary = create_frequency_dict(wordlist, language)
    # print(temp_dictionary)
    frequency_list = []
    while len(temp_dictionary) > 0:
        temp_high_key = 0
        temp_high_value = 0
        for key, value in temp_dictionary.items():
            if value >= temp_high_value:
                temp_high_value = value
                temp_high_key = key
        frequency_list.append(temp_high_key)
        temp_dictionary.pop(temp_high_key)
    # print(frequency_list)
    # print(temp_dictionary)
    return frequency_list

def shorten_wordlist(wordlist, length, difficulty1, difficulty2):
    if difficulty1 == 4 or difficulty2 == 4 or difficulty1 == 0 or difficulty2 == 0:        
        shortened_wordlist = []
        for item in wordlist:
            if len(item) == length:
                shortened_wordlist.append(item)
        # print("Délka zkráceného slovníku je:", len(shortened_wordlist))
        return shortened_wordlist
    else:
        return None

def get_shortened_freq_dict(difficulty1, difficulty2, wordlist, secret_word):
    if difficulty1 == 4 or difficulty2 == 4:
        shortened_wordlist = shorten_wordlist(wordlist, len(secret_word), difficulty1, difficulty2)
        short_frequency_list = get_frequency_dictionary(shortened_wordlist)
        return short_frequency_list
    else:
        return None

def get_DB_len_dicts(wordlist):
    DB_len_dicts = {}
    delka = 1
    max_delka = len(max(wordlist, key=len))
    while delka <= max_delka:
        DB_len_dicts[delka] = []
        for item in wordlist:
            if len(item) == delka:
                DB_len_dicts[delka].append(item)
        delka += 1
    return DB_len_dicts
                    
def get_DB_freq_dicts(DB_len_dicts, language):
    DB_freq_dicts = {}
    for key, value in DB_len_dicts.items():
        DB_freq_dicts[key] = get_frequency_dictionary(value, language)
    return DB_freq_dicts

def generate_hint(secret_word_list):
    hint = []
    for item in secret_word_list:
        hint.append("_")
    return hint

def update_letters_guessed_dict(letters_guessed_dict, letter_guessed, secret_word):
    correct_guess = is_in_secretword(letter_guessed, secret_word)
    if correct_guess == True:
        temp = 0
        for item in secret_word:
            if item == letter_guessed:
                temp += 1
        letters_guessed_dict[letter_guessed] = temp
    else:
        letters_guessed_dict[letter_guessed] = 0
    return correct_guess, letters_guessed_dict
    
# Body of the game itself 
def hangman(player1, player2, difficulty1, difficulty2, attempts, wordlist, frequency_dict, DB_freq_dicts, lettersAvailable, language):
    # List of guessed letters, initially empty
    letters_guessed_dict = {}
    # list of available letters, initially all of them
    # lettersAvailable = split(string.ascii_lowercase)
    # initialize maximum number of guessess for each player as a separate variable 
    guess_left_p1 = attempts
    guess_left_p2 = attempts
    # generate a secret_word
    secret_word = select_secret_word(wordlist)
    # for difficulty 4, create a shortened vocabulary containing just the words having the same length as secret word NOTE: OBSOLETE, BECAUSE WE ARE PRE-GENRATING THEM
    shortened_wordlist = shorten_wordlist(wordlist, len(secret_word), difficulty1, difficulty2)
    # shortened_dict = get_shortened_freq_dict(difficulty1, difficulty2, wordlist, secret_word)
    # randomly determine the player who starts    
    player1_turn = bool(random.getrandbits(1))
    # play until there are players with remaining turns
    while guess_left_p1 > 0 or guess_left_p2 > 0:
        # show basic properties of the hidden word
        secret_hint = secret_word_hint(letters_guessed_dict, secret_word, player1, player2)
        # determie who plays
        if player1_turn == True and guess_left_p1 > 0:
            vyzva_selection(player1, player2, player1_turn, guess_left_p1, lettersAvailable)
            letter_guessed = guess(player1, difficulty1, guess_left_p1, wordlist, lettersAvailable, frequency_dict, DB_freq_dicts, len(secret_word), shortened_wordlist, letters_guessed_dict, secret_hint, language)
            announce_guess(player1, player2, letter_guessed, player1_turn)            
        elif player1_turn == False and guess_left_p2 > 0:
            vyzva_selection(player1, player2, player1_turn, guess_left_p2, lettersAvailable)
            letter_guessed = guess(player2, difficulty2, guess_left_p2, wordlist, lettersAvailable, frequency_dict, DB_freq_dicts, len(secret_word), shortened_wordlist, letters_guessed_dict, secret_hint, language)
            announce_guess(player1, player2, letter_guessed, player1_turn)
        else:
            print("Nikdo nemá tahy. Ale tady bych se neměl vůbec dostat :)")
        # add the letter to the list of guessed letters and check whether the letter is in the secret word
        correct_guess, letters_guessed_dict = update_letters_guessed_dict(letters_guessed_dict, letter_guessed, secret_word)
        # check whether a word had been guessed correctly
        correctly_guessed_word = word_guessed(secret_word, letters_guessed_dict)
        if correctly_guessed_word == True:
            announce_victory(player1_turn, player1, player2, secret_word)
            if player1_turn == True:
                return 1
            else:
                return 2
        # remove this letter from available letters
        lettersAvailable.remove(letter_guessed)
        # determine next turn and number of available turns for players
        player1_turn, guess_left_p1, guess_left_p2 = determination_of_next_turn(player1_turn, guess_left_p1, guess_left_p2, correct_guess)
    announce_loss(player1, player2, secret_word)    
    return 3

game()

# cProfile.run('game()')