import matplotlib.pyplot as plt 
from utils import * 
plt.style.use("fivethirtyeight")

def get_WordleColor_RGB(color_name):
    RGB_dict = {
    "green": [102,255,102],
    "gray": [190,190,190],
    "yellow": [255,255,133]}
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
  for attempt in ATTEMPTS: 
    color_sequence = get_color_sequence(attempt,mystery_word)
    plot_colors.append([get_WordleColor_RGB(color) for color in color_sequence])

  fig, ax = plt.subplots(figsize = (5,len(ATTEMPTS) + 1))
  plt.imshow(plot_colors)
  plt.axis("off")
  for attempt_idx in range(len(ATTEMPTS)):
    for letter_idx in range(TOTAL_LETTERS):
        text = ax.text(letter_idx, attempt_idx, ATTEMPTS[attempt_idx][letter_idx],
                       ha="center", va="center", color="black", fontsize = 20)
  plt.title("Mystery Word: {}".format(mystery_word), fontsize = 18)
  plt.savefig(figure_path)