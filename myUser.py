class myUser(object):
    #A user of a server, has properties:
        # A username
            # name (string)
        # an ID
            # id (string)
        # total number of words typed in messages
            # totalWords (int)
        # total number of letters in messages
            # totalLetters (int)
        # total number of messages sent
            # totalMessages (int)
        # average words per message
            # wordsPerMessage (float)
        # average letters per words
            # lettersPerWord (float)
        # upvotes given
            # upboatesGiven (int)
        # downvotes given
            # downvotesGiven (int)
        #total karma
            # karma (int)



    def __init__(self,id,name,totalMessages =0,totalWords=0,totalLetters=0,\
    wordsPerMessage=0,lettersPerWord=0,upvotesGiven=0,downvotesGiven=0,karma=0):
        self.id = id
        self.name = name
        self.totalMessages = totalMessages
        self.totalWords = totalWords
        self.totalLetters = totalLetters
        self.wordsPerMessage = wordsPerMessage
        self.lettersPerWord = lettersPerWord
        self.upvotesGiven = upvotesGiven
        self.downvotesGiven = downvotesGiven
        self.karma = karma

    def getID(self):
        return self.id

    def getName(self):
        return self.name

    def getTotalMessages(self):
        return self.totalMessages

    def getTotalWords(self):
        return self.totalWords

    def getTotalLetters(self):
        return self.totalLetters

    def getWordsPerMessage(self):
        return self.wordsPerMessage

    def getLettersPerWord(self):
        return self.lettersPerWord

    def getUpvotesGiven(self):
        return self.upvotesGiven

    def getDownvotesGiven(self):
        return self.downvotesGiven

    def getKarma(self):
        return self.karma



    #Parameter: a user object and a string
    #PostCondition: updates all member variables of given user
    def addContent(self, content):
        self.totalMessages += 1
        self.totalWords += words(content)
        self.totalLetters += letters(content)
        self.wordsPerMessage = self.totalWords / self.totalMessages
        self.lettersPerWord = self.totalLetters / self.totalWords

    #Parameter: myUser object
    #Post Condition: objects stats
    def getStats(self):
        stats = "Username: ", self.name, "\n" +\
        "Total Messages: ", self.totalMessages, "\n" +\
        "Total Words: ", self.totalWords, "\n" +\
        "Total Letters: ", self.totalLetters, "\n" +\
        "Words per Message: ", self.wordsPerMessage, "\n" +\
        "Letters per Word: ", self.lettersPerWord, "\n" +\
        "Upvotes Given: ", self.upvotesGiven, "\n" +\
        "Downvotes Given: ", self.downvotesGiven, "\n" +\
        "Karma: ", self.karma

        return stats
    def getRatio(self):
        int1 = self.upvotesGiven
        int2 = self.downvotesGiven
        i = 1
        if(int1 !=0 and int2 !=0):
            while i <= int1 or i <= int2:
                if int1 % i == 0 and int2 % i == 0:
                    int1 = int1/i
                    int2 = int2/i
                i = i +1
        return str(str(int(int1)) + ' / ' + str(int(int2)))


#Parameter: message object
#Return: an int of total words in string
def words(message):
    return len(message.split())

#Parameter: string of message
#Return: an int of total characters, whitespace excluded, in string
def letters(message):
    return len(message) - message.count(' ')
