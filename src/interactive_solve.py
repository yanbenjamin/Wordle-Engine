"""
[interactive_solve.py] This interactive command line program helps a user to solve
the Wordle by recommending guesses. It can be used for any Wordle variant with different
numbers of words to solve simultaneously (the number of allowed guesses is the number
of words plus 5). 

To run the program, use the template
    python3 interactive_solve.py [number of words to solve simultaneously]
and the program will print out instructions for inputting responses from the Wordle. 

"""

from extract_fiveletter_words import * 
from utils import *
from visualize_wordle import *

import sys 

#global parameter used for priority-weighing possible 5-letter words in the queue
HIGHEST_FREQUENCY = 1220752

def getWordFrequency(word,frequency_dict):
    return frequency_dict[word]

def getWordFrequency(word,frequency_dict):
    return frequency_dict[word]

def sortWords_byFrequency(word_list, frequency_dict):
    return sorted(word_list[:], key = lambda word: getWordFrequency(word,frequency_dict),
                          reverse = True)

def get_WordPriority(word,global_frequency_dict, wordle_appearance_dict):
    if (word not in wordle_appearance_dict):
      local_frequency = 0
    else: 
      local_frequency = wordle_appearance_dict[word]
    return local_frequency * (HIGHEST_FREQUENCY + 1) + frequency_dict[word]

def sortWords_byPriority(word_list, global_frequency_dict, wordle_appearance_dict):
    return sorted(word_list[:], key = lambda word: get_WordPriority(word,frequency_dict, wordle_appearance_dict),
                          reverse = True)

def count_words_solved(solved_states):
  solved = 0
  for state in solved_states: 
    if (state == True):
      solved += 1
  return solved

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

  return False, num_tries 


def colorSequence_isSolved(color_sequence):
    for color in color_sequence: 
        if (color != "green"):
            return False 
    return True 

"""
a more general version that handles Wordle variants with arbitrary number of words
"""
def solve_multiple_words_interactive(N, max_tries, nyt_words, frequency_dict):
  
  #introduce the user to the interactive Worldle solve
  intro_message = """
  ------------------------------------------------------------------------------------------
  Welcome to the Interactive Wordle Solver! Currently, you are requesting the program
  for a Wordle variant with {} words and {} maximum tries.

  After each guess, input the resulting Wordle color sequences as an ordered sequence of five-character strings,
  separated by spaces, with a G for green, Y for yellow, and R for gray. The program will recommend you what the 
  next guess should be from there.

  For instance, if you are playing Quordle (4 words), after seeing [green, yellow, yellow, gray, gray], 
  [green,green,green,green,green], [green,gray,gray,gray,gray], and [green,yellow,green,green,yellow] on the screen,
  you should input GYYRR GGGGG GRRRR GYGGY. Make sure to keep the order of color sequences consistent.

  Also, if a word is finished, just write GGGGG as its color sequence in the subsequent guesses. 
  ------------------------------------------------------------------------------------------ 
  """.format(N, max_tries)
  print(intro_message)
  first_attempt = input("First, make an initial guess (Recommended: SLATE, CRANE, AROSE).\nGuess #1: ").upper()
  NUM_LETTERS = 5

  #ask them to make an initial guess
  attempts_array = [first_attempt]
  remaining_word_dict = [sortWords_byFrequency(nyt_words, frequency_dict) for _ in range(N)]
  solved_states = [False for _ in range(N)]
  
  remaining_word_idxs = [i for i in range(N)]
  num_tries = 0
  while (num_tries < max_tries):

    num_tries += 1
    guess = attempts_array[-1]
    
    #input the color sequences 
    color_sequences = input("Input the Wordle Color Sequences: ").upper().split(" ")
    color_sequences = [sequence.strip() for sequence in color_sequences]
    color_translator = {"G": "green", "Y": "yellow", "R": "gray"}
    color_sequences_array = []
    for i in range(len(color_sequences)):
        color_sequences_array.append([color_translator[char] for char in color_sequences[i]])
    
    #check which words are solved / unsolved
    for word_idx in range(N):
        if (colorSequence_isSolved(color_sequences_array[word_idx]) == True and solved_states[word_idx] == False):
            solved_states[word_idx] = True 
            remaining_word_idxs.remove(word_idx)

    #reduce the remaining candidate pools to make the next guess 
    if (len(remaining_word_idxs) == 0):
      break 
    
    wordle_appearance_dict = {}
    for word_idx in remaining_word_idxs: 
      current_remaining_words = (remaining_word_dict[word_idx])[:]
      new_remaining_words = reduce_candidate_pool(current_remaining_words, guess, color_sequences_array[word_idx])
      remaining_word_dict[word_idx] = new_remaining_words

      for word in new_remaining_words: 
        if (word in wordle_appearance_dict):
          wordle_appearance_dict[word] += 1
        else:
          wordle_appearance_dict[word] = 1

    union_words = set() 
    for word_idx in remaining_word_idxs: 
      union_words = union_words.union(set(remaining_word_dict[word_idx]))
    
    word_priority_queue = sortWords_byPriority(list(union_words), frequency_dict, wordle_appearance_dict)
    if (len(word_priority_queue) > 0):
      next_guess = word_priority_queue[0]
    else:
      next_guess = guess 
    
    if (num_tries < max_tries):
      print("Recommended Next Guess: {}".format(next_guess))
      next_guess_actual = input("\nGuess #{}: ".format(num_tries + 1)).upper()
      attempts_array.append(next_guess_actual)
  
  return solved_states, num_tries, attempts_array 

if __name__ == "__main__":
    
    frequency_dict = get_WordFrequencies()
    nyt_words = get_NYTWords() 

    N = int(sys.argv[1])
    max_tries = N + 5

    solved_states, num_tries, attempts_array = solve_multiple_words_interactive(N, max_tries, nyt_words, frequency_dict)
    if (count_words_solved(solved_states) == N):
        print("\nSuccessfully solved all {} words in {} tries!".format(N, num_tries))
    else: 
        print("\nUnable to solve the {}-word Wordle :(".format(N))


