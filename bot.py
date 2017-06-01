import discord
import asyncio
import datetime
import json
from myUser import *
from helpers import *
client = discord.Client()

#Initializing list that stores myUser class members of the server
userList = []
# Keith's birthday, any old date would do
keithBDay = "1997-12-01 01:01:01.000000"
#lastMessage = string of timestamp of last Tiger 'beat it' command
lastMessage = loadStats("stats.txt",userList)
#if stats.txt is not initially empty
if type(lastMessage) is str:
    myTime = datetime.datetime.strptime(lastMessage,'%Y-%m-%d %H:%M:%S.%f')
else:
    print("set to keith's birthday")
    myTime = datetime.datetime.strptime(keithBDay,'%Y-%m-%d %H:%M:%S.%f')

@client.event
async def on_member_ban(member):
    if member.id == client.user.id:
        for channel in member.server.channels:
            await client.send_message(channel, "You dicks")

# adds messages until the last @Tiger 'beat it' command,
#   then updates the next 1000 messages
# if 'stats.txt' is completely empty, which it would be on an initial startup to a
#    new server, then the time of the last 'beat it command' is set to Keith's
#    birthday, so the first 1000 messages are added correctly, and the next 1000
#    are not updated
@client.event
async def on_ready():
    print("Logged in as " + client.user.name + ", ID = " + client.user.id)
    #goes through every channel in the server, updating karma
    for server in client.servers:
        for channel in server.channels:
            async for missedMessage in client.logs_from(channel,limit = 2000):
                client.messages.append(missedMessage)

    for server in client.servers:
        for channel in server.channels:
            if str(channel.type) == "text":
                #goes though past 1000 messages, until messages are older than last 'beat it'
                async for missedMessage in client.logs_from(channel,limit = 1000):
                    if missedMessage.timestamp > myTime:
                        print("Added " + missedMessage.author.name +"\'s message")
                        # addMessage(userList, missedMessage.author.id,\
                        #     missedMessage.author.name, missedMessage.content)
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
                                            else:
                                                updateUpvotes(userList, upvotingUsers.id, upvotingUsers.name, 'added')
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
                                            else:
                                                updateDownvotes(userList, upvotingUsers.id, upvotingUsers.name, 'added')
                                        updateKarma(userList, missedMessage.author.id, \
                                        missedMessage.author.name, "downvote", missedReaction.count)
                    else:
                        break
    for server in client.servers:
        for channel in server.channels:
            if type(lastMessage) is str:
                #counts the last 1000 messages made before Tiger last exited, undos the exit decrements with updated information
                if myTime != "":
                    async for incrementMessage in client.logs_from(channel,limit = 1000, before = myTime):
                        if incrementMessage.reactions:
                            for incrementReaction in incrementMessage.reactions:
                                if not(type(incrementReaction.emoji) is str): #checks if emoji is emoji class or str
                                    if incrementReaction.emoji.name == "upvote":
                                        upvoteList = await client.get_reaction_users(incrementReaction)
                                        #goes through people who reacted with upvote, updates their upvotesGiven
                                        for upvotingUsers in upvoteList:
                                            #if someone upvoted their own post
                                            if upvotingUsers.id == incrementMessage.author.id:
                                                for member in incrementReaction.emoji.server.members:
                                                    if member.id == incrementMessage.author.id:
                                                        await client.remove_reaction(incrementReaction.message, incrementReaction.emoji, member)
                                        updateKarma(userList, incrementMessage.author.id, incrementMessage.author.name, "upvote", incrementReaction.count)
                                        print(incrementMessage.author.name + " incremented on enter")
                                    if incrementReaction.emoji.name == "downvote":
                                        downvoteList = await client.get_reaction_users(incrementReaction)
                                        #goes through people who reacted with downvote, updates thier downvotes given
                                        for downvotingUsers in downvoteList:
                                            #if someone downvoted their own post
                                            if downvotingUsers.id == incrementMessage.author.id:
                                                for member in incrementReaction.emoji.server.members:
                                                    if member.id == incrementMessage.author.id:
                                                        await client.remove_reaction(incrementReaction.message, incrementReaction.emoji, member)
                                        updateKarma(userList, incrementMessage.author.id, incrementMessage.author.name, "downvote", incrementReaction.count)
                                        print(incrementMessage.author.name + " decremented on enter")

    print("Done Adding messages")

@client.event
async def on_reaction_add(reaction,user):
    if(reaction.emoji.name == "upvote"):
        print("upvote given")
        updateUpvotes(userList,user.id, user.name, "added")
        updateKarma(userList,reaction.message.author.id,reaction.message.author.name,"upvote")
        # prevents users from upvoting/downvoting themselves
        if(reaction.message.author.id == user.id):
            for member in reaction.emoji.server.members:
                if member.id == user.id:
                    await client.remove_reaction(reaction.message, reaction.emoji, member)
                    break

    elif reaction.emoji.name == "downvote":
        print("downvote given")
        updateDownvotes(userList,user.id,user.name, "added")
        updateKarma(userList,reaction.message.author.id,reaction.message.author.name,"downvote")
        # prevents users from upvoting/downvoting themselves
        if(reaction.message.author.id == user.id):
            for member in reaction.emoji.server.members:
                if member.id == user.id:
                    await client.remove_reaction(reaction.message, reaction.emoji, member)
                    break

@client.event
async def on_reaction_remove(reaction,user):
    if(reaction.emoji.name == "upvote"):
        print("upvote removed")
        updateUpvotes(userList, user.id, user.name, "removed")
        updateKarma(userList,reaction.message.author.id,reaction.message.author.name,"downvote")

    elif reaction.emoji.name == "downvote":
        print("downvote removed")
        updateDownvotes(userList,user.id, user.name, "removed")
        updateKarma(userList,reaction.message.author.id, reaction.message.author.name, "upvote")

@client.event
async def on_message(message):
    #runs on every message, updates users 'smarts' statistics
    for user in userList:
        if(user.id == message.author.id):
            user.addContent(message.content)
            break
    else:
        userList.append(myUser(message.author.id, message.author.name))
        userList[-1].addContent(message.content)

    # if "why tiger" in message.content.lower() or "tiger why did you beat your wife?"\
    #  in message.content.lower() or "tiger why did you beat your wife" in message.content.lower():
    #     await client.send_message(message.channel, "Not because I\'m bad at golf!")
    # #the trigger to print 'smarts' stats
    # elif message.content.lower().startswith("smarts", 0, 6):
    #     #if message contains @notificaions, will print for all mentioned
    #     if message.mentions:
    #         for user in message.mentions:
    #             for user1 in userList:
    #                 if(user1.id == user.id):
    #                     await client.send_message(message.channel, content = \
    #                         'Username: ' + user1.getName() + '\n' + \
    #                         '   Average letters per word: ' + str(user1.getLettersPerWord()) + '\n' + \
    #                         '   Average words per message: ' + str(user1.getWordsPerMessage()) + '\n' + \
    #                         '   Smarts: ' + str(((user1.getLettersPerWord() + user1.getWordsPerMessage())//2) % 10))
    #                     break
    #             else:
    #                 await client.send_message(message.channel, content = user.name + ' is apparently too dumb to have typed anything.')
    #     #if no one is mentioned, will print for message author
    #     else:
    #         for user in userList:
    #             if(user.id == message.author.id):
    #                 await client.send_message(message.channel, content = \
    #                     'Username: ' + user.getName() + '\n' + \
    #                     '   Average letters per word: ' + str(user.getLettersPerWord()) + '\n' + \
    #                     '   Average words per message: ' + str(user.getWordsPerMessage()) + '\n' + \
    #                     '   Smarts: ' + str(((user.getLettersPerWord() + user.getWordsPerMessage())//2) % 10))
    #                 break
    #the trigger to print 'karma' stats
    elif message.content.lower().startswith("karma",0,5):
        if message.mentions:
            for user in message.mentions:
                for keithUser in userList:
                    if(keithUser.id == user.id):
                        await client.send_message(message.channel, content = \
                            'Username: ' + keithUser.getName() + '\n' + \
                            # '   Approximate ratio of Upvotes/Downvotes given to others: ' + str(keithUser.getRatio()) + '\n' + \
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
                            # '   Approximate ratio of Upvotes/Downvotes given to others: ' + str(keithUser.getRatio()) + '\n' + \
                            '   Karma: ' + str(keithUser.getKarma()))
                    break
    elif "timestamp" in message.content.lower():
        await client.send_message(message.channel, str(message.timestamp))

    # on bot mention
    elif message.content.lower().strip('<>@!').startswith(str(client.user.id)):
        # I ALONE CAN TRIGGER THESE
        if(message.author.id == "165582042426376192"):
            if("beat it" in message.content.lower()):
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
                                                        print("decremented on exit")
                                            if decrementReaction.emoji.name == "downvote":
                                                for keithUser in userList:
                                                    if keithUser.id == decrementMessage.author.id:
                                                        keithUser.karma += decrementReaction.count
                                                        print("incremented on exit")


                storeStats("stats.txt",message.timestamp,userList)
                print("Exited normaly")
                await client.logout()
        if("source" in message.content.lower()[message.content.find(' '):]):
            await client.send_message(message.channel, content = "https://github.com/keithZmudzinski/Tiger-Woods-Discord-Bot")


client.run("MjEzMDIxMjIxNTk0MzMzMTg0.Co0YOQ.k0yWmRvt7BlB_HVz9ltB8fuvUos")
