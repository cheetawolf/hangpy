# Author: Ritchie Yapp
# Admin number: 2205810
import getpass
import json
import os

def updateSetting(setting):
    intBuffer = strictInput(setting) #get input through strictInput
    if intBuffer == "":
        return "Cancelling operation"
    return (f"Operation successful, {setting}: {intBuffer}", intBuffer)
   
def strictInput(msg): 
    """a function for validation, only allows a strict number
    msg = used for formatting the user input, either str attempt, words, players"""
    while True: 
        try: 
            inp = int(input(f"Enter the number of {msg}: ").strip())
            if inp == "":
                return "override" #return to the previous screen, after
            if not inp.isnumeric():
                raise ValueError
            break 
        except ValueError:
            print("Invalid input, please try again")

def addWords():
    fWords = open("./data/word_list.txt", "r")
    words = fWords.readlines()

defaultSettings = {"attempts": 3, "words": 3, "players": 4} #gameSettings() will declare global var and access this when needed
def gameSettings():
    fSettings = open("./data/game_settings.json")
    try: 
        settings = json.load(fSettings) #working dictionary
        fSettings.close()
    except json.JSONDecodeError:
        global defaultSettings
        fSettings = open("./data/game_settings.json", "w")
        json.dump(defaultSettings, fSettings, indent=4) #write the json parsed dictionary
        fSettings.close()
        settings = defaultSettings #working dictionary 
    uInp = 0
    opLog = "Game settings" #log messages after each operation
    while uInp != 4:
        os.system('cls') #called after every successful or non successful operation
        print(f"""
{opLog}

1) Number of attempts: {settings["attempts"]}
2) Number of words: {settings["words"]}
3) Number of players: {settings["players"]}
4) Exit
        """)
        while True:
            try: 
                uInp = int(input("Enter option: "))
                if uInp not in range(1, 5):
                    raise ValueError
                break
            except ValueError:
                print("Invalid input please try again")
        match uInp: #refer to above menu for match cases flow, these update the settings
            case 1: #strict inputs only, tried making it a function but this needs to work locally ugh
                opLog = updateSetting("attempts")
                if type(opLog) == tuple:
                    settings["attempts"] = opLog[1] 
                    opLog = opLog[0]
            case 2: 
                opLog = updateSetting("words")
                if type(opLog) == tuple: 
                    settings["words"] = opLog[1]
                    opLog = opLog[0]
            case 3:
                opLog = updateSetting("players")
                if type(opLog) == tuple:
                    settings["players"] = opLog[1] 
                    opLog = opLog[0] 
            

            #case 4 will break the loop and return to the main menu, clearing the terminal so no output required

    

#warning: no of words < attempts cannot be allowed as it breaks given current hangman algorithm
def auth():
    global shadowLines
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
            return True
        else: 
            print("Incorrect password")


def menu():
    #returns 1 if terminated else returns 0, to determine whether to loop
    os.system('cls')
    menuHead = "Admin panel" #to be used in adMenu as syntax bypass xd
    adMenu = f"""
{menuHead:*^20}

1. Modify game settings
2. Create new user
3. Add new words
4. Exit 
    """
    print(adMenu)
    while True:
        try: 
            uInp = int(input("Enter option: "))
            if uInp not in range(1, 5):
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
            return 1
    return 0
    

def uInit(fTime=False):
    os.system('cls')
    #fTime: indicates first time initialisation to avoid loading empty json file which also is exception in exception
    print("Create new user")
    while True:
        userName = input("\nPlease enter the admin username: ") #masks password
        global shadowLines
        if fTime != True: #no shadowLines if init so this avoids exception in the next line
            if userName in shadowLines: 
                if input("User exists in database, change password instead?\nEnter \'Y\' to proceed: ").lower().strip() != "y":
                    return 0
        while True:
            valid = 0
            userPass = getpass.getpass("Please enter the admin password: \n")
            #consider using OOP for this
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
                #these errors truth value are True by default, invalid == 1 when iterating through the keys and any truth value is 1
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
            userEmail = input("Enter your email for password recovery purposes: ")
            if input(f"Is this email correct? {userEmail} enter \'y\' to confirm").lower().strip() == "y":
                break
    #REMEMBER TO HASH YOUR SHIT HERE!!!
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

#main execution
fShadow = open("./data/shadow.json", "r")
try:
    shadowLines = json.load(fShadow) #lines buffer to save memory, instead of keeping the file open when not needed
    fShadow.close()
    authState = auth()
except json.JSONDecodeError: #this exception is raised when file is empty at worst corrupted
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
            break
else: 
    exit()
#test case password: 1Qwer$#@!