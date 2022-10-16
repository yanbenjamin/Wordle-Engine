"""
solve_dordle.py
---------------------
file that leverages the program to solve the Dordle, with the corresponding board images
saved to the "sample" directory as a filename dordle_[word1]_[word2].jpg. 
Note that solve_wordle_multiple.py generalizes the algorithm here to arbitrary words solved simultaneously. 

As a template,
    python3 solve_wordle.py [word 1] [word 2]
will attempt to solve both word1 and word2 simultaneously in 7 tries. 
"""

from extract_fiveletter_words import * 
from utils import *
from visualize_wordle import *

import sys 
import time 
import numpy as np

def getWordFrequency(word,frequency_dict):
    return frequency_dict[word]

def sortWords_byFrequency(word_list, frequency_dict):
    return sorted(word_list[:], key = lambda word: getWordFrequency(word,frequency_dict),
                          reverse = True)

def solve_two_words(word_1, word_2, nyt_words, frequency_dict, starter_word = "SLATE",visuals = False):
  
  word_1_characters = get_character_dict(word_1)
  word_2_characters = get_character_dict(word_2)

  MAX_NUM_TRIES = 7
  ATTEMPTS = [starter_word]
  
  #sort the words from most common to least common in the Wikipedia corpus 
  remaining_words_1 = sortWords_byFrequency(nyt_words, frequency_dict)
  remaining_words_2 = remaining_words_1[:]

  num_tries = 0
  solved_state_1 = False
  solved_state_2 = False

  #while we haven't exhausted all of the possible Dordle tries (7)
  while (num_tries < MAX_NUM_TRIES): 
    num_tries += 1

    #the next guess is the most common word that hasn't been ruled out yet 
    attempt = ATTEMPTS[-1]

    #determine the color sequence by comparing the attempt to the actual mystery word
    color_sequence_1 = get_color_sequence(attempt, word_1)
    color_sequence_2 = get_color_sequence(attempt, word_2)

    if (attempt == word_1):
      solved_state_1 = True
    if (attempt == word_2):
      solved_state_2 = True 
    
    if (solved_state_1 == True and solved_state_2 == True):
      #game solved 
      break
    elif (solved_state_1 == True and solved_state_2 == False):
      #only focus on Word 2 (could be recursive)
      remaining_words_2 = reduce_candidate_pool(remaining_words_2, attempt, color_sequence_2)
      if (len(remaining_words_2) > 0):
        next_attempt = remaining_words_2[0]
      else:
        next_attempt = attempt
    elif (solved_state_1 == False and solved_state_2 == True):
      #only focus on Word 1
      remaining_words_1 = reduce_candidate_pool(remaining_words_1, attempt, color_sequence_1)
      if (len(remaining_words_1) > 0):
        next_attempt = remaining_words_1[0]
      else:
        next_attempt = attempt
    else: 
      #focus on both words by priority queue ranking
      #reduce the set of possible words based on the Wordle color sequence  
      remaining_words_1 = reduce_candidate_pool(remaining_words_1, attempt, color_sequence_1)
      remaining_words_2 = reduce_candidate_pool(remaining_words_2, attempt, color_sequence_2)

      joint_words = list(set(remaining_words_1).intersection(set(remaining_words_2)))
      joint_words = sortWords_byFrequency(joint_words, frequency_dict)

      union_words = list(set(remaining_words_1).union(set(remaining_words_2)))
      union_words = sortWords_byFrequency(union_words, frequency_dict)

      if (len(joint_words) > 0):
        next_attempt = joint_words[0]
      elif (len(union_words) > 0):
        next_attempt = union_words[0]
      else: 
        next_attempt = attempt 

    if (num_tries < MAX_NUM_TRIES):
      ATTEMPTS.append(next_attempt)
  
  if (visuals == True):
    #determine where to save the figures
    current_file = os.path.abspath(__file__)
    Wordle_directory = "/".join(current_file.split("/")[:-2])
    FIGURES_DIR = Wordle_directory + "/sample"
    figure_path = os.path.join(FIGURES_DIR, "dordle_{}_{}.jpg".format(word_1, word_2))
    plot_dordle_fullboard(word_1, word_2, ATTEMPTS, figure_path)
  
  return solved_state_1, solved_state_2, num_tries, ATTEMPTS

 
if __name__ == "__main__": 
    frequency_dict = get_WordFrequencies()
    nyt_words = get_NYTWords() 

    word_1 = sys.argv[1].upper() 
    word_2 = sys.argv[2].upper()

    state_1, state_2, num_tries, attempts = solve_two_words(word_1,word_2,nyt_words,frequency_dict,visuals=True)
    