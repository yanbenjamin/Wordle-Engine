"""
performance_test.py
---------------------
More comprehensive performance tests than simulate_wordle.py. 

For Wordle, it tests all 2309 possible words. As the number of combinations scaled mostly
exponentially with the number of words per combination, then for Dordle and onward, 
this program will run 10,000 simulations due to efficiency and calculate 
the percentage of word tuples solved, the number of guesses, etc. 

However, a function is provided for running all possible combinations, although its
runtime will be poor for larger Wordle variants. 
"""

from solve_wordle_multiple import solve_multiple_words, count_words_solved
import time 
import tqdm 
from tqdm import tqdm 
import numpy as np
from extract_fiveletter_words import *
import sys
import itertools 

"""
runs the Wordle engine on all possible combinations of a certain number of words. 
"""
def run_all(num_words, nyt_words, frequency_dict):
    successes = 1
    total_time = 0 
    total_words_in_bank = len(nyt_words) 
    max_tries = num_words + 5
   
    #generates all possible combinations of words within the NYT word bank
    word_tuples_idx = itertools.combinations(list(range(total_words_in_bank)), num_words)

    guesses_data = [] #each entry in this list is a tuple of the form (word combination, mumber of guesses)
    num_iterations = sum(1 for _ in itertools.combinations(list(range(total_words_in_bank)), num_words))

    print("Applying the Wordle Engine to all {} combinations of {} words".format(num_iterations, num_words))
    for idx_tuple in tqdm(word_tuples_idx): 
        #for each tuple, run and time the Wordle engine. 
        word_tuple = [nyt_words[idx] for idx in list(idx_tuple)]
        init_time = time.time() 
        solved_states, num_tries, attempts_array = solve_multiple_words(1, word_tuple, nyt_words, frequency_dict, max_tries)
        final_time = time.time()
        total_time += (final_time - init_time)

        if (count_words_solved(solved_states) == num_words):
            successes += 1
            guesses_data.append((word_tuple, num_tries))
        else: 
            guesses_data.append((word_tuple, -1)) #-1 denotes FAIL 
    
    return successes, total_time, guesses_data 

"""
helper function analyze the output list guesses_data in the run_all() functions, 
and calculate a discrete distribution of the number of guesses needed. 
"""
def get_guess_statistics(num_words, guesses_data):  
    histogram_guesses = {num_guesses: 0 for num_guesses in range(1,num_words + 6)}
    histogram_guesses[-1] = 0 #counting failed cases
    for guess_tuple in guesses_data: 
        word_tuple, num_guesses = guess_tuple 
        histogram_guesses[num_guesses] += 1 
    return histogram_guesses

"""
runs the Wordle engine on a high number of randomly selected combinations of a certain number of words.
More practical for larger Wordle variants. 
"""
def run_simulations(num_words, num_simulations, nyt_words, frequency_dict):
  successes = 0
  total_time = 0
  total_guesses = 0

  #number of allowed guesses is the number of words to be solved plus five. 
  max_tries = num_words + 5 

  #runs the specified number of simulations, choosing a set of Wordle words randomly. 
  for _ in tqdm(range(num_simulations)): 
    words = np.random.choice(nyt_words, size = num_words, replace = False)
    init_time = time.time() 
    solved_states, num_tries, attempts_array = solve_multiple_words(num_words, words, nyt_words, frequency_dict, max_tries)
    final_time = time.time()
    if (count_words_solved(solved_states) == num_words):
      successes += 1
    total_time += (final_time - init_time)
    total_guesses += num_tries 
  
  return successes, total_time, total_guesses

if __name__ == "__main__": 
    frequency_dict = get_WordFrequencies()
    nyt_words = get_NYTWords()

    #runs over all possible Wordle words and prints out a distribution of the number of guesses. 
    num_words = 1
    successes, total_time, guesses_data = run_all(num_words,nyt_words,frequency_dict)
    total_runs = len(guesses_data)
    histogram_guesses = get_guess_statistics(num_words,guesses_data)
    print("# Guesses  | Percentage of {}-Word Combinations".format(num_words))
    for num_guesses in range(1,num_words + 6): 
        print("{:10d} | {:.6}".format(num_guesses, histogram_guesses[num_guesses] / total_runs * 100))
    print("        >6 | {:.6}".format(histogram_guesses[-1] / total_runs * 100))
