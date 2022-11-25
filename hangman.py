# Author: Ritchie Yapp
# Admin number: 2205810
import random 
import os

def editLine(guess, map, line):
    """_summary_
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
def main():
    gameWords = ["deer", "peko", "suisex", "suipiss"] #sampled number of words from word list, number of words predefined
    totalAttempt = 4 #predefined setting
    score = 0
    hangman = """
  ________
 |        |
 |      {1}
 |   {2}{1}{3}
 |    {4} {5}
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
            playerName = input("Enter your player name: ") 
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
        attemptLine = ["_" for i in attemptWord] #attemptLine: user output showing guesses and blanks
        mistakeLetters = []
        while mistakes < 5: 
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
                score += 2
            else:
                mistakeLetters.append(guess)
                mistakes += 1
            
    #return details
main()
# write
logFile = open("./data/game_log.txt", "w")
logFile.close()

