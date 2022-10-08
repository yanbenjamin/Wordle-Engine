"""
[solve_wordle.py] file that leverages the program to solve the Wordle
for mystery words that are provided via command line. The corresponding results (Wordle boards)
are saved in jpg files to the "sample" directory. 

As a template,
    python3 solve_wordle.py [word 1] [word 2] ... [word n]
will attempt all n words that are valid NYT Wordle solutions, and save the resulting boards
with the naming format wordle_[mystery word].jpg. 
"""

from extract_fiveletter_words import * 
from utils import *
from visualize_wordle import *

import sys 

MAIN_DIR = "/Users/benjaminyan/Desktop/Projects/Wordle-Solver"
FIGURES_DIR = MAIN_DIR + "/sample"
SRC_DIR = MAIN_DIR + "/src"
DOCS_DIR = MAIN_DIR + "/docs"

def getWordFrequency(word,frequency_dict):
    return frequency_dict[word]

def solve_word(mystery_word, nyt_words, frequency_dict, starter_word = "SLATE",visuals = False):
  mystery_word_letters = get_character_dict(mystery_word)
  MAX_NUM_TRIES = 6 
  ATTEMPTS = [starter_word]
  
  #sort the words from most common to least common in the Wikipedia corpus 
  remaining_words = sorted(nyt_words[:], key = lambda word: getWordFrequency(word,frequency_dict),
                          reverse = True)
  num_tries = 0
  wordle_solved_state = False

  #while we haven't exhausted all of the possible Wordle tries (6)
  while (num_tries < MAX_NUM_TRIES): 
    num_tries += 1

    #the next guess is the most common word that hasn't been ruled out yet 
    attempt = ATTEMPTS[-1]

    #determine the color sequence by comparing the attempt to the actual mystery word
    color_sequence = get_color_sequence(attempt, mystery_word)
    if (attempt == mystery_word): #solved!
      wordle_solved_state = True
      break
    
    #reduce the set of possible words based on the Wordle color sequence 
    remaining_words = reduce_candidate_pool(remaining_words, attempt, color_sequence)
    
    if (len(remaining_words) == 0): #error checking 
      ATTEMPTS.append(ATTEMPTS[-1])

    #add the most common word (according to Wikipedia corpus frequency) still remaining 
    if (num_tries < MAX_NUM_TRIES): #if we are still allowed to guess
        ATTEMPTS.append(remaining_words[0])
  
  #at the end, plot the Wordle result to a .jpg file using Matplotlib
  if (visuals == True):
    figure_path = os.path.join(FIGURES_DIR, "wordle_{}.jpg".format(mystery_word))
    plot_wordle_fullboard(mystery_word, ATTEMPTS, figure_path)

  return wordle_solved_state, num_tries, ATTEMPTS 

if __name__ == "__main__": 
    frequency_dict = get_WordFrequencies()
    nyt_words = get_NYTWords() 
    
    #runs through each word inputted in the command line, and attempt to solve for it
    #in Wordle using SLATE as the starting word
    for word in sys.argv[1:]: 
        word = word.upper()
        if (word not in nyt_words):
            print("Word {} not in possible NYT Wordle solutions".format(word))
            continue 
        solved_state, num_tries, attempts = solve_word(word, nyt_words, frequency_dict, visuals = True)
       
        if (solved_state == True):
            #successful solve!
            figure_path = os.path.join(FIGURES_DIR, "wordle_{}.jpg".format(word))
            print("Solved {} in {} Tries -> Board Result saved to {}".format(
                word, num_tries, figure_path))
        else:
            print("Unable to solve {} (last guess: {}) -> Board Result saved to {}".format(
                word, attempts[-1], figure_path))
