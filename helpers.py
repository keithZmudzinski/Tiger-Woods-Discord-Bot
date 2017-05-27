from myUser import *

#storeStats and loadStats used to save/populate the userList of myUser class objects

#storeStats runs when '@tiger... take a break' is sent
def storeStats(fileName, statsList):
    file = open(fileName, "w")
    for user in statsList:
        file.write(user.id + '\n')
        file.write(user.name + '\n')
        file.write(str(user.totalMessages) + '\n')
        file.write(str(user.totalWords) + '\n')
        file.write(str(user.totalLetters) + '\n')
        file.write(str(user.wordsPerMessage) + '\n')
        file.write(str(user.lettersPerWord) + '\n')
        file.write(str(user.upvotesGiven) + '\n')
        file.write(str(user.downvotesGiven) + '\n')
        file.write(str(user.karma) + '\n')
    file.close()
#runs on startup
def loadStats(fileName, userList):
    try:
        file = open(fileName,"r")
    except:
        print("Error opening" + str(fileName))

    while True:
        id = file.readline().strip('\n')
        if(id == ""):   #if it reads in an empty line, it has reached end of file
            return
        name = file.readline().strip('\n')
        totalMessages = int(file.readline().strip('\n'))
        totalWords = int(file.readline().strip('\n'))
        totalLetters = int(file.readline().strip('\n'))
        wordsPerMessage = float(file.readline().strip('\n'))
        lettersPerWord = float(file.readline().strip('\n'))
        upvotesGiven = int(file.readline().strip('\n'))
        downvotesGiven = int(file.readline().strip('\n'))
        karma = int(file.readline().strip('\n'))

        userList.append(myUser(id,name,totalMessages,totalWords,totalLetters,\
        wordsPerMessage,lettersPerWord,upvotesGiven,downvotesGiven,karma))
    file.close()

def updateUpvotes(userList,idToCheck, name, type):
    for keithUser in userList:
        if(keithUser.id == idToCheck):
            if type == "added":
                keithUser.upvotesGiven += 1
            else:
                keithUser.upvotesGiven -=1
            break
    else:
        if type == "added":
            userList.append(idToCheck, name, upvotesGiven = 1)
            
def updateDownvotes(userList,idToCheck, name, type):
    for keithUser in userList:
        if(keithUser.id == idToCheck):
            if type == "added":
                keithUser.downvotesGiven += 1
            else:
                keithUser.downvotesGiven -= 1
            break
    else:
        if type == "added":
            userList.append(idToCheck, name, downvotesGiven = 1)

def updateKarma(userList, idToCheck, name, type):
    if(type == "upvote"):
        for keithUser in userList:
            if(keithUser.id == idToCheck):
                keithUser.karma += 1
                break
        else:
            userList.append(idToCheck, name, karma = 1)
    else:
        for keithUser in userList:
            if keithUser.id == idToCheck:
                keithUser.karma -= 1
                break
        else:
            userList.append(idToCheck, name, karma = -1)
