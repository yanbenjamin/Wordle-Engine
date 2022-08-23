from extract_fiveletter_words import * 
from utils import *
from visualize_wordle import *

import sys 

MAIN_DIR = "/Users/benjaminyan/Desktop/Projects/Wordle-Solver"
FIGURES_DIR = MAIN_DIR + "/sample"
SRC_DIR = MAIN_DIR + "/src"
DOCS_DIR = MAIN_DIR + "/docs"
TESTS_DIR = MAIN_DIR + "/tests"

def getWordFrequency(word,frequency_dict):
    return frequency_dict[word]

def solve_word_interactive(nyt_words, frequency_dict, user_loop = False):
  MAX_NUM_TRIES = 6
  num_tries = 0
  
  #edit intro message for user in the loop
  intro_message = """
  ------------------------------------------------------------------------------------------
  Welcome to the Interactive Wordle Solver!

  After each guess, input the resulting Wordle color sequence as a five-character string,
  with a G for green, Y for yellow, and R for gray. The program will recommend you what the 
  next guess should be from there.

  For instance, after seeing green, yellow, yellow, gray, gray on your Wordle screen,
  you should input GYYRR.  
  ------------------------------------------------------------------------------------------ 
  """
  print(intro_message)
  ATTEMPTS = [input("First, make an initial guess (Recommended: SLATE, CRANE, AROSE).\nGuess #1: ").upper()]
  NUM_LETTERS = 5
  remaining_words = sorted(nyt_words[:], key = lambda word: getWordFrequency(word,frequency_dict),
                          reverse = True)
  
  success_bool = False
  while (num_tries < MAX_NUM_TRIES): 
    num_tries += 1
    attempt = ATTEMPTS[-1]

    letter_colors_string = input("Input the Wordle Color Sequence: ").upper()
    color_translator = {"G": "green", "Y": "yellow", "R": "gray"}
    color_sequence = [color_translator[letter] for letter in letter_colors_string]

    if (color_sequence == ["green" for _ in range(NUM_LETTERS)]):
        return True, num_tries 

    #reduce the set of remaining words, and produce 
    #the most likely one of them by frequency

    remaining_words = reduce_candidate_pool(remaining_words, attempt, color_sequence)
    if (len(remaining_words) > 0):
        next_guess = remaining_words[0]
        #ATTEMPTS.append(remaining_words[0])
    else:
        next_guess = ATTEMPTS[-1]
        #ATTEMPTS.append(ATTEMPTS[-1])

    if (num_tries < MAX_NUM_TRIES):
        if (user_loop == False):
            ATTEMPTS.append(next_guess)
            print("\nGuess #{}: {}".format(num_tries + 1, ATTEMPTS[-1]))
        else:
            #possiblity for overrule 
            print("Recommended Next Guess: {}".format(next_guess))
            next_guess_actual = input("\nGuess #{}: ".format(num_tries + 1)).upper()
            ATTEMPTS.append(next_guess_actual)

      #next_attempt = input("Guess # ").upper()
    #ATTEMPTS.append(remaining_words[0])

  #ATTEMPTS.append(getMystery())

  return False, num_tries 

  #also return the num_tries 

if __name__ == "__main__":
    frequency_dict = get_WordFrequencies()
    nyt_words = get_NYTWords() 
    solve_state, num_tries = solve_word_interactive(nyt_words, frequency_dict, True)
    if (solve_state == True):
        print("\nSolved the Wordle in {}!".format(num_tries))
    else:
        print("\nThe program was unable to solve the Wordle :(")
