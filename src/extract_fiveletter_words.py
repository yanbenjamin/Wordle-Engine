"""
extract_fiveletter_words.py
-------
this file chiefly contains two functions for (1) gathering a 
list of NYT solution words and (2) ranking these words by
their frequencies inside a massive text corpus. These functions are deployed in the Wordle 
program to help optimize and refine the word search during each guess. 
"""

import os 

"""
this function outputs a dictionary where the keys are five-letter English words
and the corresponding values are their frequencies across Wikipedia articles 

file source for word frequencies from: https://en.lexipedia.org/
"""
def get_WordFrequencies():
    #find the location of the word frequency file using os knowledge of the filetree
    #file is located in the sample folder with name en_words_1_1-64.txt
    current_file = os.path.abspath(__file__)
    Wordle_directory = "/".join(current_file.split("/")[:-2])
    filename = Wordle_directory + "/docs/en_words_1_1-64.txt"

    fiveletter_word_frequencies = {}
    with open(filename,"r") as file:
        td_idf = file.readlines() 
        for word_parse in td_idf: 
            #each entry in the table has the form 
            #[word] [number of letters] [total frequency across texts] [number of texts it appears in]
            word_parse = word_parse.replace("\n","").strip()
            word_split = word_parse.split(" ")
            word = word_split[0].upper()
            num_letters = int(word_split[1])
            word_frequency = int(word_split[2])

            #add {word: frequency} to dictionary only if it is a five-letter word
            if (num_letters == 5):
                fiveletter_word_frequencies[word] = word_frequency

    return fiveletter_word_frequencies

"""
extracts a list of all possible five-letter word solutions to the NYT wordle,
all converted to upper-case letters: [...,"ADIEU",...]

list of NYT words is sourced from: https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee
"""
def get_NYTWords():
    #find the location of the word list file using os knowledge of the filetree
    #file is located in the sample folder with name wordle-nyt-answers-alphabetical.txt
    current_file = os.path.abspath(__file__)
    Wordle_directory = "/".join(current_file.split("/")[:-2])
    filename = Wordle_directory + "/docs/wordle-nyt-answers-alphabetical.txt"

    nyt_words = []
    with open(filename,"r") as file: 
        contents = file.readlines()
        #each line contains a separate five-letter word
        for word in contents: 
            word = word.replace("\n","").strip()
            nyt_words.append(word.upper())
    return nyt_words

"""
main function for debugging / testing

making sure that the program correctly extracts the NYT solution words
and ranks them in order of their frequencies in a large text corpus. 
"""
if __name__ == "__main__":

    frequency_dict = get_WordFrequencies()
    nyt_words = get_NYTWords() 
    sorted_nyt_words = sorted(nyt_words)

    print("Number of NYT Five-Letter Words: {}".format(len(nyt_words)))
    print("First 10 Words: {}".format(sorted_nyt_words[:10]))
    print("Last 10 Words: {}\n".format(sorted_nyt_words[-10:]))

    print("Top 10 Highest Frequency Five-Letter English Words")
    print("----------------------------------------------")
    print("WORD  | FREQUENCY")
    for word, frequency in sorted(frequency_dict.items(), 
                                key = lambda item: item[1], reverse = True)[:10]:
        print("{} | {}".format(word,frequency))