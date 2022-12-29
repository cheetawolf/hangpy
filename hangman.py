"""Author: Ritchie Yapp
Admin number: 2205810
game attempt as in guess x number of words, either correct or incorrect is the outcome 
"""
import random 
import os
import json

with open("./data/game_settings.json") as fSettings:
    settings = json.load(fSettings) #is a constant

def main(num):
    #num is player num, this function plays for one player, with number of attempts with number of mistakes
    global settings
    with open("./data/word_list.txt", "r") as fWords:
        gameWords = fWords.readlines() #regenerates every player
    totalAttempt = int(settings["attempts"])
    score = 0
    fills = [] #ascii art of the hangman to be filled out throughout the game
    hangman = """
  ________
 |        |
 |      {fills[0]}
 |   {fills[2}{fills[1]}{fills[3]}
 |    {fills[4]} {fills[5]}
 |
_|_
| |_________
|           |
|___________|

    """#format brackets indicate which is filled after incorrect attempt
    #input player name for game set
    while True: 
        try: 
            #playerName (str): only upper/lowercase letters '-' '/'
            playerName = input(f"Player {num} name: ") 
            for char in playerName:
                if not (char.isalpha()) and char not in ['-', '/']: #validate
                    raise ValueError
            break
        except ValueError:
            print("Please try again.\n")

    for attempt in range(totalAttempt):
        mistakes = 0
        guesses = []
        #"removes" a random word from game set words and puts it in attemptWord, 
        attemptWord = "".join(gameWords.pop(random.randrange(len(gameWords))).split())
        wordMap = {} #wordMap (dict): key= unique letter in word, value= (list) all indexes of letter
        for i in range(len(attemptWord)):
            wordMap[attemptWord[i]] = []
        for i in range(len(attemptWord)):
            wordMap[attemptWord[i]].append(i) #separate for loops to prevent overwriting
        attemptLine = ["_"] * attemptWord #attemptLine: user output showing guesses and blanks
        mistakeLetters = []
        while mistakes < int(settings["mistakes"]): 
            os.system('cls')
            print(f"""
H A N G M A N

Player: {playerName}
{attempt + 1} of {totalAttempt}

{hangman}

Incorrect letters: {" ".join(mistakeLetters)} ({mistakes})

{"".join(attemptLine)}
""")        
            #if correctly guessed, output requires to show full game before this action
            if "".join(attemptLine) == attemptWord:
                print(f"Congratulations. The Secret Word is \"{attemptWord}\". Your score after this set is {score}")
                while True:
                    try: 
                        retryIn = input("Enter [Y] to play again or [N] to quit: ").lower()
                        if retryIn == "n":
                            exit()
                        elif retryIn != "y": #to avoid user conflict using other inputs
                            raise ValueError
                        break #the input is y to flow here
                    except ValueError:
                        print("Invalid input please try again\n")
            #game input
            while True:
                try:
                    guess = input("Select a valid character [a-z, \']: ")
                    if guess == '' or len(char) != 1:
                        raise ValueError #iteration through the input will not catch these cases
                    for char in guess:
                        if (not char.isalpha() and char != '\''):
                            raise ValueError
                    break
                except ValueError:
                    print("Invalid input!\n")
            if guess in attemptWord: #correct letter
                guesses.append(guess)
                attemptLine = editLine(guess, wordMap, attemptLine)
                score += int(settings["score"])
            else:
                mistakeLetters.append(guess)
                mistakes += 1
            
def editLine(guess, map, line):
    """ for editing the word to be guessed in the ouput in dashes and guesses
    Args:
        guess (str): 1 char guess
        map (dict): key=letter present, value=list of indexes of letter
        line (list): current output of guesses in the word
    Returns:
        line: newly updated line after guess
    """
    updateIndexes = map[guess] #if guess e in deer, update indexes [1, 2]
    for ind in range(len(updateIndexes)):
        line[updateIndexes[ind]] = guess
    return line

    #return details
for i in range(int(settings["players"])):
    main(i + 1)
# write
logFile = open("./data/game_log.txt", "w")
logFile.close()
