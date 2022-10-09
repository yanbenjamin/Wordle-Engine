# Wordle Engine 
## Description
This Wordle engine is an automated Python program for playing the Wordle game. Using "SLATE" as the starting word, it is able to solve $96.1$ percent of the possible words in Wordle with an average of $\sim 3.9$ guesses.
<br/>
<br/>
It has been extended with reasonable accuracy to variants Dordle (2 words simultaneously in 7 tries), Quordle (4 words in 9 tries), and Octordle (8 words in 13 tries). More generally, it applies to any variant with $M$ words and $M+5$ word tries. Below are sample results of the engine on Wordle and Dordle, respectively. More quantitative results are shown below. 
### Sample Result from Wordle
![image of Wordle result](./sample/wordle_DREAM.jpg?raw=true)
### Sample Result from Dordle
![image of Dordle result](./sample/dordle_ISLET_POINT.jpg?raw=true)
## Dataset Credits
As acknowledgement, this project makes use of the NYT Wordle list of 2309 five-letter words obtained from [link](https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee), as well as calculated word frequencies across the Wikipedia corpus from [link](https://en.lexipedia.org/). 
## Performance 


## Accessing and Using the Engine Locally 
### Cloning and Navigating Repository 
In the directory you want the repository to be located, run:
'''
git clone https://github.com/yanbenjamin/Wordle-Engine.git
cd Wordle-Engine 
'''
There is a lightweight, custom Conda environment provided in local_environment.yml. If you have Conda installed, to ensure having the correct dependencies, run: 
'''
conda env create -f local_environment.yml
conda activate wordle_engine
conda deactivate #after use 
'''
If you don't have Conda, most Python and Linux distributions have the necessary packages, which can be found in the .yml file.  In this repository, you will find the list of NYT Wordle words and word frequency data located in the docs folder, the main code for running the engine in the src folder, and a few Wordle board visualizations from example runs in the sample folder. 

### Using the Interactive Command Line Tool 
### Producing Wordle Board Visualizations 

## Engine Implementation Summary
As a sketch, the algorithm uses a priority queue that ranks word candidates first based on (1) the number of mystery words they could still be (haven't been ruled out yet) and then (2) their frequency in a gigantic text corpus. The more mystery words a candidate could still match, the higher the ranking; if two candidates are tied in the former metric, the candidate with the highest frequency in the corpus is given a higher ranking. For each guess, the algorithm receives feedback in the form of letter color sequences from the Wordle game, trims the sets of candidates for each mystery word accordingly, re-ranks the candidates, and selects the highest-ranking one. 

<!---
Automated Python program for playing the Wordle game, as well as the popular variants Dordle (2 words at the same time), Quordle (4), and Octordle (8)---and even the Sedecordle (16) mayhem. More generally, it supports Wordle variants with an arbitrary number of words, with the maximum allowed tries being 5 greater than the number of words. 
Using the starting word "SLATE", this solves the NYT one-word Wordle for 96.1% of the possible 5-letter solutions, with an average of ~3.9 guesses. 
As citation, this work makes use of the NYT Wordle list of 2309 five-letter words obtained from [], as well as calculated word frequencies across the Wikipedia corpus ascertained from []


## Sample Result from Wordle
![image of Wordle result](./sample/wordle_DREAM.jpg?raw=true)

## Sample Result from Dordle
![image of Dordle result](./sample/dordle_ISLET_POINT.jpg?raw=true)
--->


