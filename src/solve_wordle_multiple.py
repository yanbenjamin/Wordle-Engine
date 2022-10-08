"""
solve_wordle_mutiple.py
---------------------
Programmed to play any Wordle variant with M words and M + 5 tries using a priority queue
that ranks word candidates first based on the number of mystery words they could still be 
(haven't been ruled out yet) and then their frequency in a gigantic text corpus. 

This file can be run for debugging / testing, with 
  python3 solve_wordle_multiple.py [word 1] ... [word m]
attempting to solve all m words simultaneously in m + 5 tries. 
"""

from extract_fiveletter_words import * 
from utils import *
from visualize_wordle import *

import sys 
import time 
import numpy as np
from tqdm import tqdm

#global variable used for weighing words in the priority queue. 
HIGHEST_FREQUENCY = 1220752

def getWordFrequency(word,frequency_dict):
    return frequency_dict[word]

def sortWords_byFrequency(word_list, frequency_dict):
    return sorted(word_list[:], key = lambda word: getWordFrequency(word,frequency_dict),
                          reverse = True)

"""
word priority is first determine by the number of mystery words it can still match (hasn't
been ruled out yet) and then by its frequency in a massive text corpus. 
"""
def get_WordPriority(word,global_frequency_dict, wordle_appearance_dict):
    if (word not in wordle_appearance_dict):
      local_frequency = 0
    else: 
      local_frequency = wordle_appearance_dict[word]
    return local_frequency * (HIGHEST_FREQUENCY + 1) + global_frequency_dict[word]

def sortWords_byPriority(word_list, global_frequency_dict, wordle_appearance_dict):
    return sorted(word_list[:], key = lambda word: get_WordPriority(word,global_frequency_dict, wordle_appearance_dict),
                          reverse = True)

def count_words_solved(solved_states):
  solved = 0
  for state in solved_states: 
    if (state == True):
      solved += 1
  return solved

"""
plays Wordle with an arbitrary number of words with a variable number of max tries,
and returns which words were solved as a boolean array, the number of tries, and the attempts. 
"""
def solve_multiple_words(N, mystery_words, nyt_words, frequency_dict, max_tries, starter_word = "SLATE"):

  if (N != len(mystery_words)):
    raise ValueError("len(words) ({}) and N ({}) must be equal".format(len(mystery_words), N))

  word_characters = [get_character_dict(word) for word in mystery_words]
  attempts_array = [starter_word]
  remaining_word_dict = {
    word: sortWords_byFrequency(nyt_words, frequency_dict) for word in mystery_words
  }
  solved_states = [False for _ in range(N)]
  num_tries = 0

  while (num_tries < max_tries):

    num_tries += 1
    guess = attempts_array[-1]
    color_sequences = {
      word: get_color_sequence(guess, word) for word in mystery_words}
    
    for word_idx, word in enumerate(mystery_words):
      if (word == guess and solved_states[word_idx] == False):
        solved_states[word_idx] = True
        #axe them from the list
    
    #reduce the remaining candidate pools to make the next guess 
    remaining_words = [word for word_idx, word in enumerate(mystery_words) if solved_states[word_idx] == False]
    if (len(remaining_words) == 0):
      break 
    
    wordle_appearance_dict = {}
    for word in remaining_words: 
      current_remaining_words = (remaining_word_dict[word])[:]
      new_remaining_words = reduce_candidate_pool(current_remaining_words, guess, color_sequences[word])
      remaining_word_dict[word] = new_remaining_words

      for word in new_remaining_words: 
        if (word in wordle_appearance_dict):
          wordle_appearance_dict[word] += 1
        else:
          wordle_appearance_dict[word] = 1

    union_words = set() 
    for word in remaining_words: 
      union_words = union_words.union(set(remaining_word_dict[word]))
    
    word_priority_queue = sortWords_byPriority(list(union_words), frequency_dict, wordle_appearance_dict)
    if (len(word_priority_queue) > 0):
      next_guess = word_priority_queue[0]
    else:
      next_guess = guess 
    
    if (num_tries < max_tries):
      attempts_array.append(next_guess)
  
  return solved_states, num_tries, attempts_array 

if __name__ == "__main__": 
  frequency_dict = get_WordFrequencies()
  nyt_words = get_NYTWords() 

  mystery_words = [word.strip().upper() for word in sys.argv[1:]]
  N = len(mystery_words)
  max_tries = N + 5 
  solved_states, num_tries, attempts_array = solve_multiple_words(N, mystery_words, nyt_words, frequency_dict, max_tries)
  num_words_solved = count_words_solved(solved_states)
  if (num_words_solved == N):
    print("Program was able to solve mystery words {} in {} guesses".format(mystery_words, num_tries))
  else:
    print("Program was unable to solve mystery words {}.".format(num_tries))
  print("Here were the guesses: {}".format(attempts_array))



  
