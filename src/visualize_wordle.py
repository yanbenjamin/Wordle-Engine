"""
[visualize_wordle.py] auxiliary file used for producing visual Wordle
and Dordle boards that resemble the actual website format. 
"""

import matplotlib.pyplot as plt
import sys
import os 
from utils import * 
plt.style.use("fivethirtyeight")

FIGURE_DIR = "/Users/benjaminyan/Desktop/Projects/Wordle-Solver" + "/sample"

"""
function to translate a named color on the Wordle board to an RGB tuple. 
"""
def get_WordleColor_RGB(color_name):
    RGB_dict = {
    "green": [102,255,102],
    "gray": [190,190,190],
    "yellow": [255,255,133],
    "white": [255,255,255]}
    if (color_name in list(RGB_dict.keys())):
        return RGB_dict[color_name]
    raise ValueError("Invalid Wordle Color")

"""
this function plots the Wordle result on a matplotlib board, where the inputs are
the mystery word as a string, and ATTEMPTS is an ordered list of the guesses (up to 6),
from first to last
"""
def plot_wordle_fullboard(mystery_word, ATTEMPTS, figure_path): 
  TOTAL_LETTERS = 5
  plot_colors = []

  #extracts the letter color sequences needed to visualize the Wordle board 
  for attempt in ATTEMPTS: 
    color_sequence = get_color_sequence(attempt,mystery_word)
    plot_colors.append([get_WordleColor_RGB(color) for color in color_sequence])
  
  fig, ax = plt.subplots(figsize = (5,len(ATTEMPTS) + 1))
  plt.imshow(plot_colors)
  plt.axis("off")
  #labels each cell in the board with the correct letter and color. 
  for attempt_idx in range(len(ATTEMPTS)):
    for letter_idx in range(TOTAL_LETTERS):
        text = ax.text(letter_idx, attempt_idx, ATTEMPTS[attempt_idx][letter_idx],
                       ha="center", va="center", color="black", fontsize = 20)
  plt.title("Mystery Word: {}".format(mystery_word), fontsize = 18)
  plt.savefig(figure_path)

"""
this function plots the Dordle (two words simultaneously) board, incorporating
a similar design to the Wordle board except with two columns, one for each word. 
"""
def plot_dordle_fullboard(word_1, word_2, ATTEMPTS, figure_path): 
  TOTAL_LETTERS = 5
  TOTAL_TRIES = 7
  plot_colors_1 = []
  plot_colors_2 = []

  word_1_solved = False 
  word_2_solved = False 
  num_attempts_to_solve_1 = None
  num_attempts_to_solve_2 = None

  for attempt_number, attempt in enumerate(ATTEMPTS): 

    if (word_1_solved == True): 
      plot_colors_1.append([get_WordleColor_RGB("white") for _ in range(TOTAL_LETTERS)])
    else: 
      color_sequence_1 = get_color_sequence(attempt,word_1)
      plot_colors_1.append([get_WordleColor_RGB(color) for color in color_sequence_1])

    if (word_2_solved == True):
      plot_colors_2.append([get_WordleColor_RGB("white") for _ in range(TOTAL_LETTERS)])
    else: 
      color_sequence_2 = get_color_sequence(attempt,word_2)
      plot_colors_2.append([get_WordleColor_RGB(color) for color in color_sequence_2])

    #check if solved 
    if (word_1 == attempt and word_1_solved == False):
      word_1_solved = True 
      num_attempts_to_solve_1 = attempt_number + 1
    if (word_2 == attempt and word_2_solved == False):
      word_2_solved = True 
      num_attempts_to_solve_2 = attempt_number + 1
  
  if (num_attempts_to_solve_1 == None):
    num_attempts_to_solve_1 = 7
  if (num_attempts_to_solve_2 == None):
    num_attempts_to_solve_2 = 7

  #ensures that each cell in the Dordle board will be assigned the correct color. 
  for _ in range(TOTAL_TRIES - len(ATTEMPTS)):
    plot_colors_1.append([get_WordleColor_RGB("white") for _ in range(TOTAL_LETTERS)])
    plot_colors_2.append([get_WordleColor_RGB("white") for _ in range(TOTAL_LETTERS)])

  fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize = (10,6))
  ax[0].imshow(plot_colors_1)
  ax[0].axis("off")

  #labels each cell in the board for the first word with the corresponding color and letter. 
  for attempt_idx in range(num_attempts_to_solve_1):
    for letter_idx in range(TOTAL_LETTERS):
        text = ax[0].text(letter_idx, attempt_idx, ATTEMPTS[attempt_idx][letter_idx],
                       ha="center", va="center", color="black", fontsize = 20)
  ax[0].set_title("Mystery Word: {}".format(word_1), fontsize = 18)
  
  #labels each cell in the board for the second word with the corresponding color and letter. 
  ax[1].imshow(plot_colors_2)
  ax[1].axis("off")
  for attempt_idx in range(num_attempts_to_solve_2):
    for letter_idx in range(TOTAL_LETTERS):
        text = ax[1].text(letter_idx, attempt_idx, ATTEMPTS[attempt_idx][letter_idx],
                       ha="center", va="center", color="black", fontsize = 20)
  ax[1].set_title("Mystery Word: {}".format(word_2), fontsize = 18)

  plt.savefig(figure_path)

"""
main function, primarily to be used for debugging

for command line, write
  python3 visualize_wordle.py [mystery word 1] [mystery word 2] [guess 1] [guess 2] ... [guess n]
to produce a Dordle board visual and save it to the "sample" directory. 
"""
if __name__ == "__main__":
  word_1 = sys.argv[1]
  word_2 = sys.argv[2] 
  ATTEMPTS = sys.argv[3:]
  if (len(ATTEMPTS) > 7):
    ATTEMPTS = ATTEMPTS[:7]
  figure_path = os.path.join(FIGURE_DIR, "dordle_{}_{}.jpg".format(word_1,word_2))
  plot_dordle_fullboard(word_1,word_2,ATTEMPTS,figure_path)