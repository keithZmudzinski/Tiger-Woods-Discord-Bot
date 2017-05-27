# Tiger-Woods-Discord-Bot
Simple bot to meme with friends

Commands:
  'smarts @userName'  : prints the users average words per message, letters per word, and 'smarts' stat (two previous stats averaged and                           %10). Can take multiple user mentions, will print sequentially.
  'karma @userName'   : prints users total number of upvotes given to other users, downvotes given, and their karma. Can take multiple                             user mentions, will print sequentially.
Background Processes:
  smarts              : For every message sent, increments total number of messages sent for the sender, and the number of words in that                           message. Used to calculate 'smarts' stat.
  karma               : When a reaction is added or removed to a message, if that reaction is 'upvote' or 'downvote', the karma of the                             author of that message will be adjusted accordingly, and the user that reacted will have his 'upvotesGiven' or                             'downvotesGiven' stat adjusted accordingly as well.
