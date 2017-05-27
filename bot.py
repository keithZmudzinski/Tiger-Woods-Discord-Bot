import discord
import asyncio
import json
from myUser import *
from helpers import *
client = discord.Client()

#Initializing list that stores myUser class members of the server
userList = []
loadStats("stats.txt",userList)

#gets the missed messages until message.author == Tiger bot
@client.event
async def on_ready():
    print("Logged in as " + client.user.name + ", ID = " + client.user.id)
    for server in client.servers:
        for channel in server.channels:
            async for missedMessage in client.logs_from(channel,limit = 500):
                if missedMessage.author.id != client.user.id:
                    print("Added " + missedMessage.author.name +"\'s message")
                    addMessage(userList, missedMessage.author.id, missedMessage.author.name,\
                     missedMessage.content)
                    if missedMessage.reactions:
                        for missedReaction in missedMessage.reactions:
                            if not(type(missedReaction.emoji) is str):
                                if missedReaction.emoji.name == "upvote":
                                    updateKarma(userList,missedMessage.author.id,\
                                    missedMessage.author.name,"upvote",missedReaction.count)

                                if missedReaction.emoji.name == "downvote":
                                    updateKarma(userList, missedMessage.author.id, \
                                    missedMessage.author.name, "downvote", missedReaction.count)
                else:
                    break

@client.event
async def on_reaction_add(reaction,user):
    print("reacted")
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

    if "why tiger" in message.content.lower() or "tiger why did you beat your wife?"\
     in message.content.lower() or "tiger why did you beat your wife" in message.content.lower():
        await client.send_message(message.channel, "Not because I\'m bad at golf!")
    #the trigger to print 'smarts' stats
    elif message.content.lower().startswith("smarts", 0, 6):
        #if message contains @notificaions, will print for all mentioned
        if message.mentions:
            for user in message.mentions:
                for user1 in userList:
                    if(user1.id == user.id):
                        await client.send_message(message.channel, content = \
                            'Username: ' + user1.getName() + '\n' + \
                            '   Average letters per word: ' + str(user1.getLettersPerWord()) + '\n' + \
                            '   Average words per message: ' + str(user1.getWordsPerMessage()) + '\n' + \
                            '   Smarts: ' + str(((user1.getLettersPerWord() + user1.getWordsPerMessage())//2) % 10))
                        break
                else:
                    await client.send_message(message.channel, content = user.name + ' is apparently too dumb to have typed anything.')
        #if no one is mentioned, will print for message author
        else:
            for user in userList:
                if(user.id == message.author.id):
                    await client.send_message(message.channel, content = \
                        'Username: ' + user.getName() + '\n' + \
                        '   Average letters per word: ' + str(user.getLettersPerWord()) + '\n' + \
                        '   Average words per message: ' + str(user.getWordsPerMessage()) + '\n' + \
                        '   Smarts: ' + str(((user.getLettersPerWord() + user.getWordsPerMessage())//2) % 10))
                    break
    #the trigger to print 'karma' stats
    elif message.content.lower().startswith("karma",0,5):
        if message.mentions:
            for user in message.mentions:
                for keithUser in userList:
                    if(keithUser.id == user.id):
                        await client.send_message(message.channel, content = \
                            'Username: ' + keithUser.getName() + '\n' + \
                            '   Approximate ratio of Upvotes/Downvotes given to others: ' + str(keithUser.getRatio()) + '\n' + \
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
                            '   Approximate ratio of Upvotes/Downvotes given to others: ' + str(keithUser.getRatio()) + '\n' + \
                            '   Karma: ' + str(keithUser.getKarma()))
                    break

    # on bot mention
    elif message.content.lower().strip('<>@!').startswith(str(client.user.id)):
        if(message.author.id == "165582042426376192"):
            if("take a break" in message.content.lower()):
                await client.send_message(message.channel, content = "sure thing boss")
                print("Exited normaly")
                storeStats("stats.txt",userList)
                await client.logout()
            elif("setup" in message.content.lower()[message.content.find(' '):]):
                # logs = yield from client.logs_from(message.chnnel)
                async for missedMessage in client.logs_from(message.channel,limit = 500):
                    print(missedMessage.author.name)
                    addMessage(userList, missedMessage.author.id, missedMessage.author.name,\
                     missedMessage.content)
                    if missedMessage.reactions:
                        for missedReaction in missedMessage.reactions:
                            if not(type(missedReaction.emoji) is str):
                                if missedReaction.emoji.name == "upvote":
                                    updateKarma(userList,missedMessage.author.id,\
                                    missedMessage.author.name,"upvote",missedReaction.count)
                            elif not(type(missedReaction.emoji) is str):
                                if missedReaction.emoji.name == "downvote":
                                    updateKarma(userList, missedMessage.author.id, \
                                    missedMessage.author.name, "downvote", missedReaction.count)
        #just has to have 'source' somewhere in the message after the @mention
        if("source" in message.content.lower()[message.content.find(' '):]):
            await client.send_message(message.channel, content = "https://github.com/keithZmudzinski/Tiger-Woods-Discord-Bot")


client.run("MjEzMDIxMjIxNTk0MzMzMTg0.Co0YOQ.k0yWmRvt7BlB_HVz9ltB8fuvUos")
