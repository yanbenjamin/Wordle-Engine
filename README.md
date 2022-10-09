# Wordle Engine 

<a name="description"></a>

## Description
This Wordle engine is an automated Python program for playing the Wordle game. Using "SLATE" as the starting word, it is able to solve $98.9$ percent of the possible words in Wordle with an average of $\sim 3.8$ guesses.
<br/>
<br/>
It has been extended with reasonable accuracy to variants Dordle (2 words simultaneously in 7 tries), Quordle (4 words in 9 tries), and Octordle (8 words in 13 tries). More generally, it applies to any variant with $M$ words and $M+5$ word tries. Below are sample results of the engine on Wordle and Dordle, respectively. More quantitative results are shown below. 
### Sample Result from Wordle
![image of Wordle result](./sample/wordle_DREAM.jpg?raw=true)
### Sample Result from Dordle
![image of Dordle result](./sample/dordle_ISLET_POINT.jpg?raw=true)

<a name="dataset"></a>

## Dataset Credits
As acknowledgement, this project makes use of the NYT Wordle list of 2309 five-letter words obtained from [link](https://gist.github.com/cfreshman/a7b776506c73284511034e63af1017ee), as well as calculated word frequencies across the Wikipedia corpus from [link](https://en.lexipedia.org/). 

<a name="performance"></a>

## Performance 
**Wordle:** For all 2309 possible words that inhabit the NYT Wordle solution list, here are the number of guesses required by the engine. 

| Engine Guess Count    | Percentage (Number) of Words  
| -------------         | ------------- 
| `1`                | 0.043 (1)
| `2`                 | 6.28 (145)   
| `3`                | 33.35 (770)    
| `4`                 | 39.84 (920)
| `5`                | 15.33 (354)         
| `6`                 | 4.03 (93)    
| `>6 (Fail)`         | 1.13 (26)                

<a name="access"></a>

## Accessing and Using the Engine Locally 

<a name="clone"></a>

### Cloning and Navigating Repository 
In the directory you want the repository to be located, run:
```
git clone https://github.com/yanbenjamin/Wordle-Engine.git
cd Wordle-Engine 
```
There is a lightweight, custom Conda environment provided in `'local_environment.yml'`. If you have Conda installed, to ensure having the correct dependencies, run: 
```
conda env create -f local_environment.yml
conda activate wordle_engine
conda deactivate
```
If you don't have Conda, most Python and Linux distributions have the necessary packages, which can be found in the .yml file.  In this repository, you will find the list of NYT Wordle words and word frequency data located in the `'docs'` folder, the main code for running the engine in the `'src'` folder, and a few Wordle board visualizations from example runs in the `'sample'` folder. The folder `'repo_images'` just stores the images found in the `'README.md'`. Additional details and documentation of each .py file are written at the top of the source code. 
<br/>
```
conda deactivate
```

<a name="applying"></a>

### Running the Algorithm on Sample Mystery Words. 
The primary file for this is `'src/solve_wordle_multiple.py'`, which works for any number of $m \geq 1$ words solved simultaneously. For example, to solve a Quordle with words LIGHT, GOLEM, PAPER, and DIZZY, run from the main folder Wordle-Engine,
```
python3 src/solve_wordle_multiple.py LIGHT GOLEM PAPER DIZZY
```
The program will output the number of guesses and the specific guesses it made. Similarly, if one wanted to a solve a three-word Wordle with CANOE, PLUMB, and WATER, they would run
```
python3 src/solve_wordle_multiple.py CANOE PLUMB WATER
```
<br/>

<a name="interactive"></a>

### Using the Interactive Command Line Tool 
This tool for playing a live Wordle game (or any variant with $M$ words and $M+5$ tries) can be found in `'src/interactive_solve.py'`. From the main folder (Wordle-Engine), run 
```
python3 src/interactive_solve.py 1
```
to play the standard Wordle. To play a variant, change the $1$ above to the number of words that are being solved simultaneously (Dordle = 2, Quordle = 4, etc). Then, the program will provide the instructions at the top for using the 
engine. A sample usage for the daly Wordle (October 8th) is shown below. Here, the colored boxes annotate where the user provides input to the program. Green boxes describe where you tell the engine which guesses you decided to make; orange boxes describe the resulting color sequences from the game (with characters G,Y,R for green, yellow, and gray, respectively). 
<br/>

![image of interactive engine for 1 word (Wordle)](./repo_images/interactive_1word.png?raw=true)

<br/>

A sample for playing the daily Quordle on October 8th is also shown below. Note that there are four color sequences per word as there are four words to solve simultaneously. The color annotations are identically applied. 

<br/>

![image of interactive engine for 4 words (Quordle)](./repo_images/interactive_4words.png?raw=true)

<br/>

<a name="visualization"></a>

### Producing Wordle Board Visualizations 
To produce visualizations like the game board on the website, the files `'src/solve_wordle.py'` and `'src/solve_dordle.py'` will come in handy. They harness plotting functions that are sourced in `'src/visualize_wordle.py'`. Currently, this repository supports plot visualization just for Wordle and Dordle. For example, from the main folder (Wordle-Engine), run 
```
python3 src/solve_wordle.py ISLET
```
This will run the Wordle engine on the word ISLET, and produce an image in `'sample/wordle_ISLET.jpg'`. Similarly, 
```
python3 src/solve_dordle.py DREAM CRANE
```
will run the two-word Wordle engine to solve DREAM and CRANE simultaneously, and produce an image in `'sample/dordle_DREAM_CRANE.jpg'`.

<a name="implementation"></a>

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


