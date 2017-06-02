import discord
import asyncio
import datetime
import json
from myUser import *
from helpers import *
client = discord.Client()


#============== INITIALIZE VARIABLES ===========================================

#file to store/load data to and from
fileName = "stats.txt"

#Initializing list that stores myUser class members of the server
userList = []

#timeOfLastExit = string of timestamp of last Tiger 'beat it' command
timeOfLastExit = loadStats(fileName,userList)

#allows for detection of failed resume in onReady
firstOnReadyCall = True

#if stats.txt is  initially empty, timeOfLastExit is None
if type(timeOfLastExit) is str:
    timeOfLastExit = datetime.datetime.strptime(timeOfLastExit,'%Y-%m-%d %H:%M:%S.%f')
else:
    print("timeOfLastExit is None")
#===============================================================================

# adds messages until the last @Tiger 'beat it' command,
#   then updates the next 1000 messages
# if 'stats.txt' is completely empty, which it would be on an initial startup to a
#    new server, then the time of the last 'beat it command' is set to Keith's
#    birthday, so the first 1000 messages are added correctly, and the next 1000
#    are not updated
@client.event
async def on_ready():
    global firstOnReadyCall
    print("Logged in as " + client.user.name + ", ID = " + client.user.id)
    for server in client.servers:
        for channel in server.channels:
            async for missedMessage in client.logs_from(channel,limit = 2000):
                client.messages.append(missedMessage)
    #loads past 1000 messages' karma
    if type(timeOfLastExit) is None:
        await loadKarma()
        firstOnReadyCall = False
    # loads past 1000 missed messages' karma and increments
    #   the karma decremented on exit
    elif firstOnReadyCall:
        print("Loading...")
        await loadKarma(AFTER = timeOfLastExit)
        await loadKarma(BEFORE = timeOfLastExit)
        firstOnReadyCall = False
    # should only be called on accidental laptop closure
    # loads past 1000 missed messages' karma
    else:
        print("failed resume caught")
        await loadKarma(AFTER = timeOfLastExit)

    print("Done adding messages")

@client.event
async def on_reaction_add(reaction,user):
    if not(type(reaction.emoji) is str):
        if(reaction.emoji.name == "upvote"):
            print("upvote given")
            updateUpvotes(userList,user.id, user.name, "added")
            updateKarma(userList,reaction.message.author.id,\
            reaction.message.author.name,"upvote")
            # prevents users from upvoting/downvoting themselves
            if(reaction.message.author.id == user.id):
                for member in reaction.emoji.server.members:
                    if member.id == user.id:
                        await client.remove_reaction(reaction.message,\
                         reaction.emoji, member)
                        break

        elif reaction.emoji.name == "downvote":
            print("downvote given")
            updateDownvotes(userList,user.id,user.name, "added")
            updateKarma(userList,reaction.message.author.id,\
            reaction.message.author.name,"downvote")
            # prevents users from upvoting/downvoting themselves
            if(reaction.message.author.id == user.id):
                for member in reaction.emoji.server.members:
                    if member.id == user.id:
                        await client.remove_reaction(reaction.message,\
                         reaction.emoji, member)
                        break

@client.event
async def on_reaction_remove(reaction,user):
    if not(type(reaction.emoji) is str):
        if(reaction.emoji.name == "upvote"):
            print("upvote removed")
            updateUpvotes(userList, user.id, user.name, "removed")
            updateKarma(userList,reaction.message.author.id,\
            reaction.message.author.name,"downvote")

        elif reaction.emoji.name == "downvote":
            print("downvote removed")
            updateDownvotes(userList,user.id, user.name, "removed")
            updateKarma(userList,reaction.message.author.id,\
            reaction.message.author.name, "upvote")

@client.event
async def on_message_delete(message):
    if message.reactions:
        for reaction in message.reactions:
            if not(type(reaction.emoji) is str): #checks if emoji is emoji class or str
                if reaction.emoji.name == "upvote":
                    updateKarma(userList, message.author.id,\
                    message.author.name, "downvote", reaction.count)
                if reaction.emoji.name == "downvote":
                    updateKarma(userList, message.author.id,\
                    message.author.name, "upvote", reaction.count)

@client.event
async def on_message(message):
    global timeOfLastExit
    timeOfLastExit = message.timestamp
    timeOfLastExit = timeOfLastExit + datetime.timedelta(microseconds = 10)
    #the trigger to print 'karma' stats
    if message.content.lower().startswith("karma",0,5):
        if message.mentions:
            for user in message.mentions:
                for keithUser in userList:
                    if(keithUser.id == user.id):
                        await client.send_message(message.channel, content = \
                            'Username: ' + keithUser.getName() + '\n' + \
                            '   Karma: ' + str(keithUser.getKarma()))
                        break
                else:
                    await client.send_message(message.channel, content = \
                    user.name + ' is a tumblr ho and therefore has no karma yet')
        #if no one is mentioned, will print for message author
        else:
            for keithUser in userList:
                if(keithUser.id == message.author.id):
                    await client.send_message(message.channel, content = \
                            'Username: ' + keithUser.getName() + '\n' + \
                            '   Karma: ' + str(keithUser.getKarma()))
                    break


    elif "timestamp" in message.content.lower():
        await client.send_message(message.channel, str(message.timestamp))

    # on bot mention
    elif message.content.lower().strip('<>@!').startswith(str(client.user.id)):
        # I ALONE CAN TRIGGER THESE
        if(message.author.id == "165582042426376192"):


            if("beat it" in message.content.lower()):
                print("Saving...")
                await storeKarma()
                storeStats(fileName,timeOfLastExit,userList)
                print("Exited normaly")
                await client.logout()


        if("source" in message.content.lower()[message.content.find(' '):]):
            await client.send_message(message.channel, content = \
            "https://github.com/keithZmudzinski/Tiger-Woods-Discord-Bot")

#=================== HELPERS THAT PERTAIN TO THE BOT ===========================

async def storeKarma():
    for server in client.servers:
        for channel in server.channels:
            if str(channel.type) == "text":
                async for decrementMessage in client.logs_from(channel,limit = 1000):
                    if decrementMessage.reactions:
                        for decrementReaction in decrementMessage.reactions:
                            if not(type(decrementReaction.emoji) is str): #checks if emoji is emoji class or str
                                if decrementReaction.emoji.name == "upvote":
                                    for keithUser in userList:
                                        if keithUser.id == decrementMessage.author.id:
                                            keithUser.karma -= decrementReaction.count
                                            # print("decremented on exit")
                                if decrementReaction.emoji.name == "downvote":
                                    for keithUser in userList:
                                        if keithUser.id == decrementMessage.author.id:
                                            keithUser.karma += decrementReaction.count

async def loadKarma(BEFORE = None, AFTER = None):
    for server in client.servers:
        for channel in server.channels:
            if str(channel.type) == "text":
                #goes though past 1000 messages, until messages are older than last 'beat it'
                async for missedMessage in client.logs_from(channel, limit = 1000, before = BEFORE, after = AFTER):
                     #if the message has reactions
                    if missedMessage.reactions:
                        for missedReaction in missedMessage.reactions:
                            if not(type(missedReaction.emoji) is str): #checks if emoji is emoji class or str
                                if missedReaction.emoji.name == "upvote":
                                    upvoteList = await client.get_reaction_users(missedReaction)
                                    #goes through people who reacted with upvote, updates their upvotesGiven
                                    for upvotingUsers in upvoteList:
                                        #if someone upvoted their own post
                                        if upvotingUsers.id == missedMessage.author.id:
                                            for member in missedReaction.emoji.server.members:
                                                if member.id == missedMessage.author.id:
                                                    await client.remove_reaction(missedReaction.message, missedReaction.emoji, member)
                                    updateKarma(userList,missedMessage.author.id,\
                                    missedMessage.author.name,"upvote",missedReaction.count)

                                if missedReaction.emoji.name == "downvote":
                                    upvoteList = await client.get_reaction_users(missedReaction)
                                    #goes through people who reacted with downvote, updates thier downvotes given
                                    for upvotingUsers in upvoteList:
                                        #if someone downvoted their own post
                                        if upvotingUsers.id == missedMessage.author.id:
                                            for member in missedReaction.emoji.server.members:
                                                if member.id == missedMessage.author.id:
                                                    await client.remove_reaction(missedReaction.message, missedReaction.emoji, member)
                                    updateKarma(userList, missedMessage.author.id, \
                                    missedMessage.author.name, "downvote", missedReaction.count)

client.run("MjEzMDIxMjIxNTk0MzMzMTg0.Co0YOQ.k0yWmRvt7BlB_HVz9ltB8fuvUos")
