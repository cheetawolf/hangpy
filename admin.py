"""Author: Ritchie Yapp
Admin number: 2205810

Known issues: (SECURITY) Deleting ./data/shadow.json results in a password reset

TODO: add password recovery using email collection
consider merging updateSetting() and strictInput()
(IMPORTANT) hash shadow.json
(not important) accept end dates that are later than start date but end dates 
before start dates will just not produce any output
"""
import getpass
import datetime
from datetime import date
import json
import os
import time
lg = "" #global variable is the user logged in used for uRem() where it needs only password input

def updateSetting(setting):
    """ updates the setting in gameSettings() where setting is a key in 
    the json file ./data/game_log.json
    Args:
        setting (str): a key in the json file ./data/game_log.json
    Returns:
        "Cancelling operation": if user has chosen to abort during this function
        the gameSettings() function receiving this value will 
        abort and print this message in the main menu as it returns

        (f"Operation successful, {setting}: {intBuffer}", intBuffer): A successful 
        operation will return a time where index 0 is a message to be printed in the 
        main menu as it exits. Index 1 is the integer (input done and checked valid by strictInput())
        which the user input as the new value for the setting.
    """
    intBuffer = strictInput(setting) #get int input through strictInput
    if intBuffer == "override": #special str value to cancel operation
        return "Cancelling operation"
    return (f"Operation successful, {setting}: {intBuffer}", intBuffer)
   
def strictInput(msg): 
    """a function for allowing a strict number with a special return feature if blank
    msg = used for formatting the user input, either str attempt, words, players"""
    while True: 
        try: 
            inp = input(f"Enter the number of {msg}, press enter to cancel: ").strip()
            if inp == "":
                return "override" #return to the previous screen, after
            else: 
                inp = str(inp)
            if not inp.isnumeric(): #think about it, -1 players would not sound good
                raise ValueError
            elif int(inp) < 1:
                raise ValueError
            break 
        except ValueError:
            print("Invalid input, please try again")
    return inp 

def csValid(string):
    #function to check the validity of a comma separated input for the words
    #string parameter: the input string should only contain words and commas
    #returns a truth of the validty and if true will return a list of words stripped and separated, else blank
    for ch in string:
        if (ch in [" ", ","] or ch.isalpha()) == False: #invalid input case 
            return [False]
    string = string.split(",") #now a list 
    for i in range(len(string)): #trim leading spaces
        string[i] = string[i].strip() 
    return [True, string]

#gameSettings() will declare global var and access this when needed
defaultSettings = {"attempts": "3", "max": "30", "players": "4", "mistakes": "5", "score": "2"} 
def gameSettings():
    """
    Subfunction, option 1 of the main admin menu, modifies the hangman game settings
    or clears the leaderboard or prints logs filtered by a valid date.
    No arguments or output 
    """
    global shadowLines, lg
    fSettings = open("./data/game_settings.json")
    try: 
        opLog = "Game settings" #log messages after each operation
        settings = json.load(fSettings) #attempt to catch errors
        fSettings.close()
    except json.JSONDecodeError:
        global defaultSettings
        fSettings = open("./data/game_settings.json", "w")
        json.dump(defaultSettings, fSettings, indent=4) #write the json parsed dictionary
        fSettings.close()
        settings = defaultSettings #working dictionary 
        opLog = "Game settings, using default settings due to first time use or corruption in game_settings.json"
    uInp = 0
    while uInp != 8:
        os.system('cls') #called after every successful or non successful operation
        print(f"""
{opLog}

1) Number of attempts: {settings["attempts"]}
2) Max score: {settings["max"]}
3) Number of players on leaderboard: {settings["players"]}
4) Mistakes per attempt: {settings["mistakes"]}
5) Score increment per correct guess: {settings["score"]}
6) Clear leaderboard
7) Print report
8) Save and exit
        """)
        while True:
            try: 
                uInp = int(input("Enter option: "))
                if uInp not in range(1, 9):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input please try again")
        hSettings = "" #setting buffer, is a key of json settings
        match uInp: #refer to above menu for match cases flow, these update the settings
            case 1: #strict inputs only, tried making it a function but this needs to work locally ugh
                hSettings = "attempts"
            case 2: 
                hSettings = "max"
            case 3:
                hSettings = "players"
            case 4: 
                hSettings = "mistakes"
            case 5:
                hSettings = "score"
            case 6:
                while True:
                    userPass = getpass.getpass("Please enter the admin password (enter to exit): \n")
                    if userPass == "":
                        break
                    if userPass == shadowLines[lg]["password"]:
                        opLog = "Leaderboard has been reset"
                        with open("./data/game_log.json", "w") as wList:
                            json.dump({}, wList)
                        break
                    else:
                        print("Password is incorrect")
            case 7:
                os.system('cls')
                while True:
                    try:
                        sDate = input("Input start date (YYYY-MM-DD) or enter to use default date: ")
                        if sDate == "":
                            sDate = "1970-01-01"
                        eDate = input("Input end date (YYYY-MM-DD) or enter to use today's date: ")
                        if eDate == "":
                            eDate = str(date.today())
                        for bDate in (sDate, eDate):
                            if bDate[4] != "-" or bDate[7] != "-" or len(bDate) != 10:
                                raise ValueError #must use '-' to split
                            year, month, day = bDate.split('-')
                            datetime.datetime(int(year), int(month), int(day))
                        break
                    except ValueError:
                        print("Invalid input please try again")
                #overwrite the str dates as a datetime object
                year, month, day = sDate.split('-')
                sDate = datetime.datetime(int(year), int(month), int(day))
                year, month, day = eDate.split('-')
                eDate = datetime.datetime(int(year), int(month), int(day))
                with open("./data/game_log.json") as gLog:
                    gameLog = json.load(gLog)
                os.system('cls')
                refName = "name" #used as a pointer to settings as strings in fstrings conflict in next line
                refScore = "score"
                refDate = "date"
                for key in gameLog.keys():
                    dateBuffer = gameLog[key]["date"]
                    year, month, day = dateBuffer.split('-')
                    dateBuffer = datetime.datetime(int(year), int(month), int(day))
                    if dateBuffer >= sDate and dateBuffer <= eDate: #compare
                        print(f"#{key}: {gameLog[key][refName]}, Score: {gameLog[key][refScore]}, Date: {gameLog[key][refDate]}")
                input("Press any key to return: ")
        if hSettings != "":
            opLog = updateSetting(hSettings)
            if type(opLog) == tuple:
                settings[hSettings] = opLog[1] 
                opLog = opLog[0]
    fSettings = open("./data/game_settings.json", "w")
    json.dump(settings, fSettings, indent=4) #write the json parsed dictionary
    fSettings.close()
    
#warning: no of words < attempts cannot be allowed as it breaks given current hangman algorithm
#EDIT: has been resolved on client side, now terminates the program and requires admin to input 
# (words > attempt)
def auth():
    """_summary_
    Returns:
        (boolean value of True if username and password is correct, else False)
    """
    global shadowLines, lg
    while True:
        while True:
            user = input("Please enter the admin username or enter to exit: ")
            if user == "":
                return False
            elif user not in shadowLines.keys():
                print("User not found.")
            else:
                break
        userPass = getpass.getpass("Please enter the admin password: ")
        if userPass == shadowLines[user]["password"]:
            lg = user
            return True
        else: 
            print("Incorrect password")

def menu():
    """
    No arguments
    Prints menu, takes in an input within the function, calls subfunctions based on the input 
    returns: 0 or 1, 0 will tell the program (in the main function last few lines)
    """
    os.system('cls')
    menuHead = "Admin panel" #to be used in adMenu as syntax bypass xd
    adMenu = f"""
{menuHead:*^20}

1. Modify game settings
2. Create new user
3. Add new words
4. Remove user
5. Remove words
6. Exit 
    """
    print(adMenu)
    while True:
        try: 
            uInp = int(input("Enter option: "))
            if uInp not in range(1, 7):
                raise ValueError
            break
        except ValueError:
            print("Invalid input please try again")
    match uInp:
        case 1:
            gameSettings()
        case 2:
            uInit(False) #false as successful login suggests no init required
        case 3:
            addWords()
        case 4:
            uRem()
        case 5:
            wRem()
        case 6: 
            return 1
    return 0

def addWords():
    """add words to ./data/word_list.txt, no input
    no output
    """
    os.system('cls')
    with open("./data/word_list.txt", "r") as fWords:
        words = fWords.readlines()
    wStream = "".join(words)
    for i in range(len(words)): #remove \n
        words[i] = words[i][:-1]
    while True:
        print(f"Current list of words: \n{wStream}")
        csInp = input("Enter words to be added separated by a comma: ")
        wordSpace = csValid(csInp) #index 0 is the truth value of valid, 1 is the list of words
        if wordSpace[0]:
            nWords = wordSpace[1] #words to be appended 
            break
        else:
            os.system('cls')
            print('Invalid input please try again')
    os.system('cls')
    fWords = open("./data/word_list.txt", "a")
    for i in nWords:
        if i not in words: #prevents repeating words
            fWords.write(i + "\n")
            print(f"'{i}' has been added")
        else:
            print(f"'{i}' already exists")
    fWords.close()
    time.sleep(2)

def wRem():
    #void function to remove words in ./data/word_list.txt
    os.system('cls')
    fWords = open("./data/word_list.txt")
    words = fWords.readlines()
    wStream = "".join(words)
    while True:
        print(f"Current list of words: \n{wStream}")
        csInp = input("Enter words to be removed separated by a comma (Enter to exit): ")
        if csInp == "":
            return
        wordSpace = csValid(csInp)
        if wordSpace[0]:
            break
        else:
            os.system('cls')
            print("Invalid input please try again")
    os.system('cls')
    for i in range(len(words)): #remove \n
        words[i] = words[i][:-1]
    for word in wordSpace[1]:
        try:
            del(words[words.index(word)])
            print(f"'{word}' has been deleted")
        except ValueError:
            print(f"'{word}' could not be deleted, word not found")
    fWords = open("./data/word_list.txt", "w")
    for i in words:
        fWords.write(i + "\n")
    fWords.close()
    time.sleep(2)

def uRem():
    #void function to remove user in ./data/shadow.json, no output nor args 
    os.system('cls')
    global shadowLines, lg
    while True:
        userPass = getpass.getpass("Please enter the admin password (enter to exit): \n")
        if userPass == "":
            return
        if userPass == shadowLines[lg]["password"]:
            break
        else:
            print("Password is incorrect")
    while True:
        uName = input("Enter the username of the user to remove (enter to exit): ")
        if uName == "":
            return
        elif uName == lg:
            print("Cannot remove user that is currently logged on now. Contact your administrator.")
        else:
            if uName in shadowLines.keys():
                proc = input(f"Enter \'Y\' to confirm the deletion of {uName}. This action is irreversible: ") #input to confirm action
                os.system('cls')
                if proc.lower().strip() == "y":
                    del(shadowLines[uName])
                    fShadow = open("./data/shadow.json", "w+")
                    json.dump(shadowLines, fShadow, indent=4) 
                    fShadow.close()
                    print("User has been deleted.")
                    time.sleep(2)
                    return
                else:
                    print("Operation cancelled")
                    time.sleep(2)
                    return
            else:
                print("User does not exist") #lg should be in the shadowLines.keys() so it will never print out both error messages
    
def uInit(fTime=False):
    """ void function to create a user and append to 
    fTime: indicates first time initialisation to avoid loading empty json file which also is exception in exception
    no output"""
    os.system('cls')
    if fTime:
        print("File empty, performing initialisation")
    print("Create new user")
    global shadowLines, lg
    while True:
        userName = input("\nPlease enter the admin username: ") #masks password
        if fTime != True: #no shadowLines if init so this avoids exception in the next line
            if userName in shadowLines: 
                if input("User exists in database, change password instead?\nEnter \'Y\' to proceed: ").lower().strip() != "y":
                    return
        while True:
            valid = 0
            userPass = getpass.getpass("Please enter the admin password: \n")
            #consider using OOP for this?
            reqs = {
  "number": {
    "truth": 1,
    "msg": "Password does not have one number"
  },
  "special": {
    "truth": 1,
    "msg": "Password does not have one special character"
  },
  "alphaU": {
    "truth": 1,
    "msg": "Password does not have one uppercase character"
  },
  "alphaL": {
    "truth": 1,
    "msg": "Password does not have one lowercase character"
  },
  "length": {
    "truth": 1,
    "msg": "Password is not 4-20 characters long"
  }
}
            #stages of verification: turns truth in 
            if len(userPass) >= 4 and len(userPass) <= 20:
                reqs["length"]["truth"] = 0
            for char in userPass:
                #these errors truth value are True by default, invalid == 1 
                # when iterating through the keys and any truth value is 1
                if char.isdigit():
                    reqs["number"]["truth"] = 0
                elif char.islower():
                    reqs["alphaL"]["truth"] = 0
                elif char.isupper():
                    reqs["alphaU"]["truth"] = 0
                elif char in ["!","@","#","$","%"]: #warning: inefficent having all chars do this comparison 
                    reqs["special"]["truth"] = 0
            for key in reqs:
                if reqs[key]["truth"] == 1:
                    print(reqs[key]["msg"])
                    valid = 1
            if valid == 0:
                break
        if getpass.getpass("Re-enter the password to confirm creation: ") == userPass: #confirmation of creation is true 
            break
        else:
            print("Password does not match, try again.\n")
    while True:
        while True:
            userEmail = input("Enter your email for password recovery purposes: ")
            if "@" in list(userEmail):
                break
            else:
                print("Input email address does not contain \'@\'")
        if input(f"\nIs this email correct? {userEmail} enter \'y\' to confirm: ").lower().strip() == "y":
            break
    #REMEMBER TO HASH HERE!!!
    data = {userName: {"password": userPass, "email": userEmail}}
    if not fTime:
        #consider reading shadowLines here instead of using the start of program state of the file
        with open("./data/shadow.json") as fShadow:
            shaBuffer = json.load(fShadow) #update in json file
        shaBuffer.update(data) #append, if user exists then overwrites, updates pass
        with open("./data/shadow.json", "w") as fShadow:
            json.dump(shaBuffer, fShadow, indent=4)
        shadowLines = shaBuffer #update global run-time shadow data
    else: #if init is true
        with open("./data/shadow.json", "w") as fShadow:
            json.dump(data, fShadow, indent=4) #include indent? write the json parsed dictionary
        shadowLines = data #run-time shadow data only has one entry 
        lg = userName

#main execution
fShadow = open("./data/shadow.json", "r")
try:
    shadowLines = json.load(fShadow) #lines buffer to save memory, instead of keeping the file open when not needed
    fShadow.close()
    if shadowLines == {}: 
        raise Exception
    authState = auth()
except (json.JSONDecodeError, Exception): #this exception is raised when file is empty at worst corrupted
    fShadow.close()
    #consider writing code to make an empty file for anticorruption
    initMsg = "\nFirst time initialisation" #to work around the syntax accepting only identifiers
    print(f"{initMsg:*^20}")
    uInit(True)
    with open("./data/shadow.json") as fShadow:
        shadowLines = json.load(fShadow) #lines buffer to save memory, instead of keeping the file open when not needed
    authState = True #will grant access as auth not needed for init, MAKE SURE NOBODY CAN GET HERE
if authState: #successful authentication returns true else terminates program
    while True:
        if menu() == 1: 
            break #normal program termination 
else: 
    exit()
