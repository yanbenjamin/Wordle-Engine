"""
[performance_wordle] Runs performance simulations for Wordle, Dordle (2 words at a time),
Quordle (4), Octordle (8), and Sedecordle (16). 
"""

from solve_wordle_multiple import solve_multiple_words, count_words_solved
import time 
import tqdm 
from tqdm import tqdm 
import numpy as np
from extract_fiveletter_words import *
import sys

"""
"""
def simulate_multiple_wordle(N, num_simulations, nyt_words, frequency_dict):
  successes = 0
  total_time = 0

  #number of allowed guesses is the number of words to be solved plus five. 
  max_tries_dict = {1: 6, 2: 7, 4: 9, 8: 13, 16: 21}
  if (N not in max_tries_dict):
    raise ValueError("N must be in {1,2,4,8}")
  
  #runs the specified number of simulations, choosing a set of Wordle words randomly. 
  for _ in tqdm(range(num_simulations)): 
    words = np.random.choice(nyt_words, size = N, replace = False)
    init_time = time.time() 
    solved_states, num_tries, attempts_array = solve_multiple_words(N, words, nyt_words, frequency_dict, max_tries_dict[N])
    final_time = time.time()
    if (count_words_solved(solved_states) == N):
      successes += 1
    total_time += (final_time - init_time)
  
  return successes, total_time

if __name__ == "__main__":

  frequency_dict = get_WordFrequencies()
  nyt_words = get_NYTWords() 

  if (len(sys.argv) < 2):
    num_simulations = 10000
  else:
    num_simulations = int(sys.argv[1]) #default 10000

  print("Wordle Simulations\n--------------------------------------")
  successes, total_time = simulate_multiple_wordle(1, num_simulations, nyt_words, frequency_dict)
  print("Wordle Accuracy: {:2f}%".format(successes / num_simulations * 100))
  print("Wordle Average Time Per Problem: {:3f} s".format(total_time / num_simulations))

  print("\nDordle Simulations\n--------------------------------------")
  successes, total_time = simulate_multiple_wordle(2, num_simulations,nyt_words, frequency_dict)
  print("Dordle Accuracy: {:2f}%".format(successes / num_simulations * 100))
  print("Dordle Average Time Per Problem: {:3f} s".format(total_time / num_simulations))

  num_simulations = 1000
  print("\nQuordle Simulations\n--------------------------------------")
  successes, total_time = simulate_multiple_wordle(4, num_simulations,nyt_words, frequency_dict)
  print("Quordle Accuracy: {:2f}%".format(successes / num_simulations * 100))
  print("Quordle Average Time Per Problem: {:3f} s".format(total_time / num_simulations))

  
  print("\nOctordle Simulations\n--------------------------------------")
  successes, total_time = simulate_multiple_wordle(8, num_simulations,nyt_words, frequency_dict)
  print("Octordle Accuracy: {:2f}%".format(successes / num_simulations * 100))
  print("Octordle Average Time Per Problem: {:3f} s".format(total_time / num_simulations))

  print("\nSedecordle Simulations\n--------------------------------------")
  successes, total_time = simulate_multiple_wordle(16, num_simulations,nyt_words, frequency_dict)
  print("Sedecordle Accuracy: {:2f}%".format(successes / num_simulations * 100))
  print("Sedecordle Average Time Per Problem: {:3f} s".format(total_time / num_simulations))