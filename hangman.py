"""Author: Ritchie Yapp
Admin number: 2205810
game attempt as in guess x number of words, either correct or incorrect is the outcome 

Known issues: (Decorative) Hangman ASCII art only consists of 6 characters so total attempts that are not 
a multiple of 6 will result in the last character loading in a different trigger interval 
from others. 

TODO: IMPORTANT SCORES VIEWING, CLEARING AND FILTERING BY DATE

(Decorative) Screen clearing does not work well in Visual Studio Code terminal
"""
import random 
import os
import json
from datetime import date

with open("./data/game_settings.json") as fSettings:
    settings = json.load(fSettings) #is a constant

def main(num):
    #returns (score, name, today's date)
    #num is player num, this function plays for one player, with number of attempts with number of mistakes
    global settings
    with open("./data/word_list.txt", "r") as fWords:
        gameWords = fWords.readlines() #regenerates every player
    totalAttempt = int(settings["attempts"])
    tMistakes = int(settings["mistakes"])
    score = 0
    trigger = [(tMistakes // 6) * a for a in range(1,6)] + [tMistakes] #attempt number to show the hangman ascii,
    cFills = ["o", "-", "|", "-", "/", "\\"] #const full hangman characters to be filled from indexes 0 to 5 (start to finish)
    hangman = """
  ________
 |        |
 |        {}
 |      {}{}{}
 |       {} {}
 |
_|_
| |_________
|           |
|___________|

    """
    #format brackets indicate which is filled after incorrect attempt
    #input player name for game set
    while True: 
        try: 
            #playerName (str): only upper/lowercase letters '-' '/'
            playerName = input(f"Player {num} name: ") 
            for char in playerName:
                if not (char.isalpha()) and char not in ['-', '/']: #validate player name
                    raise ValueError
            break
        except ValueError:
            print("Please try again.\n")
    #iterate through number of attempts
    for attempt in range(totalAttempt):
        fills = [""] * 6 #ascii art of the hangman to be filled out throughout the game
        mistakes = 0
        guesses = []
        #"removes" a random word from game set words and puts it in attemptWord, 
        attemptWord = "".join(gameWords.pop(random.randrange(len(gameWords))).split())
        wordMap = {} #wordMap (dict): key= unique letter in word, value= (list) all indexes of letter
        for i in range(len(attemptWord)):
            wordMap[attemptWord[i]] = []
        for i in range(len(attemptWord)):
            wordMap[attemptWord[i]].append(i) #separate for loops to prevent overwriting
        attemptLine = ["_"] * len(attemptWord) #attemptLine: user output showing guesses and blanks
        mistakeLetters = []
        while mistakes < tMistakes: 
            os.system('cls')
            print(f"""
H A N G M A N

Player: {playerName}
{attempt + 1} of {totalAttempt}

{hangman.format(fills[0], fills[1], fills[2], fills[3], fills[4], fills[5])}

Incorrect letters: {" ".join(mistakeLetters)} ({mistakes}/{tMistakes})

{"".join(attemptLine)}
""")        
            #if correctly guessed, output requires to show full game before this action
            if "".join(attemptLine) == attemptWord:
                print(f"Congratulations. The Secret Word is \"{attemptWord}\". Your score after this set is {score}")
                if attempt + 1 != totalAttempt: # if attempt is ending no need to ask for inp
                    while True:
                        try: 
                            retryIn = input("Enter [Y] to play again or [N] to quit: ").lower()
                            if retryIn == "n":
                                #IMPORTANT - SEARCH FOR DATE WITH "Date: " as playerName Date is allowed
                                return {"name": playerName, "score": score, "date": str(date.today())}#terminates the player run
                            elif retryIn != "y": #to avoid user conflict using other inputs
                                raise ValueError
                            break #the input is y to flow here and break validation
                        except ValueError:
                            print("Invalid input please try again\n")
                break #final termination of attempt
            #game input
            while True:
                try:
                    guess = input("Select a valid character [a-z, \']: ")
                    if guess == '' or len(guess) != 1:
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
                if mistakes in trigger: #check if output hangman art needs to be updated
                    cNo = trigger.index(mistakes) #ascii art index to be drawn
                    fills[cNo] = cFills[cNo] #get character from complete lookup table cFills
        #attempt has ended, post processing
        if mistakes == tMistakes:
            print(f"You didnt guess the word. The Secret Word is \"{attemptWord}\". Your score after this set is {score}")
            if attempt + 1 != totalAttempt: # if attempt is ending no need to ask for inp
                while True:
                    try: 
                        retryIn = input("Enter [Y] to play again or [N] to quit: ").lower()
                        if retryIn == "n":
                            return {"name": playerName, "score": score, "date": str(date.today())}#terminates the player run
                        elif retryIn != "y": #to avoid user conflict using other inputs
                            raise ValueError
                        break #the input is y to flow here and break validation
                    except ValueError:
                        print("Invalid input please try again\n")

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

def lBoardPos(lb, ap):
    #updates ./data/game_log.json and keeps it sorted according to points
    #uses the principle of insertion sorting, goes down from pos 1, saves resources on adm side
    #if score is even, the existing entries will be higher than the latest entry
    #lb, the current leaderboard, ap is the appending player
    if lb == {}:
        lb = {"1": ap} #first entry
        with open("./data/game_log.json", "w") as logFile:
            json.dump(lb, logFile, indent=4)
            return
    else: #existing entries
        pos = "last"
        lPos = len(lb) #last position
        for i in range(1, lPos + 1): 
            if ap["score"] > lb[str(i)]["score"]:
                pos = str(i)
                break
        print(pos)
        if pos == "last": #append
            lPos += 1
            lb[str(lPos)] = ap
        else: #insert after moving all keys 1 index forward starting from last
            for i in range(lPos, int(pos) - 1, -1): #includes the old position of the new score to not be overwritten
                lb[str(i + 1)] = lb.pop(str(i))
            lb[pos] = ap
        with open("./data/game_log.json", "w") as logFile:
            json.dump(lb, logFile, indent=4)
            return
                


#START
os.system('cls') #clears prev cmd lines
playerCount = 0 #player number during the run 
while True:
    playerCount += 1
    gSum = main(playerCount) #game log returned after player termination, dictionary stored in gSum 
    # write
    with open("./data/game_log.json") as logFile:
        try:
            lBoard = json.load(logFile)
        except json.JSONDecodeError:
            lBoard = {}
    
    os.system('cls')
    lBoardPos(lBoard, gSum)
    refName = "name" #used as a pointer to settings as strings in fstrings conflict in next line
    refScore = "score"
    refSettings = "players"
    refDate = "date"
    print("Game Summary: \n" + f"Name: {gSum[refName]}, Score: {gSum[refScore]}, Date: {gSum[refDate]}")
    print(f"\nTop {settings[refSettings]} players:")
    for i in range(int(settings["players"])):
        print(lBoard[i], end="") #TODO: UNSORTED
  
