import discord
import markovify
import random
import json
import sentenceHelpers
import memeImg
import sys
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()

# TODO REFACTOR REFACTOOOOR
BOT_TOKEN = os.getenv('BOT_TOKEN')
LOCAL_PATH = os.getenv('LOCAL_PATH')

# init memes
memer = memeImg.MemeImgs()
memer.setTemplates()

# init leaderboards
def getLeaderboards(path):
    leaderboard_file = open(path)
    leaderboard = json.load(leaderboard_file)
    leaderboard_file.close

    return leaderboard

global LEADERBOARD
LEADERBOARD = getLeaderboards(f'{LOCAL_PATH}leaderboards.json')


# dictionary containing a path to the RAW text file of a user, and
# a model that will be filled in by updateModels on start
bots = {
    'botName': {
        'path': f'{LOCAL_PATH}rawtxt/botName.txt',
        'model': None
    }
}

# Maybe this should have been an array?
bcopy = bots
bot_idx = []
for i, bot in enumerate(bcopy):
    bot_idx.append(bot)

client = commands.Bot(command_prefix='-', case_insensitive=True, )


# For creating models from raw data
def makeModel(path):
    with open(path, encoding='utf8', errors='ignore') as f:
        text = f.read()
        model = markovify.NewlineText(text)

    return model


def updateLeaderboards(path, leaderboards):
    with open(path, 'w') as updated_leaderboards:
        json.dump(leaderboards, updated_leaderboards)

    print('Leaderboards have been updated')


# creates and updates all models
def updateModels():
    for i, bot in bots.items():
        bot['model'] = makeModel(bot['path'])

    print('all bot models created')


# picks a random sentence out of the markov generated list of sentences
def randomSentence(sentences, min_range, max_range):
    randnum = random.randint(min_range, max_range)
    return sentences[randnum][0]


# makes a random post in random interavls from 3, 8 minutes
@tasks.loop(seconds=10)
async def randomPost():
    channel = client.get_channel(706429703422083153)

    randnum = random.randint(0, len(bot_idx) - 1)
    bot = bot_idx[randnum]

    sentences = sentenceHelpers.makeSentences(bots[bot]['model'], 200, 4)
    msg = randomSentence(sentences, 0, 10)

    new_interval = random.randint(3, 8)
    randomPost.change_interval(minutes=new_interval)
    print(f'new interval is: {new_interval}')
    await channel.send(msg)


# main loop, updateModels creates a markov model for each bot in bots
@client.event
async def on_ready():
    updateModels()
    randomPost.start()
    print('Bot is ready.')


# emojiName is the name of the emoji used to represent the user
@client.event
async def on_reaction_add(reaction, user):
    # lazy implementation
    global LEADERBOARD
    ppl = {
        'emojiName': 'userName',

    }
    reac = reaction.emoji
    bot = reaction.message.content.split(':')[1]

    if reac == '👍':
        LEADERBOARD[ppl[bot]] += 1
        updateLeaderboards(f'{LOCAL_PATH}leaderboards.json', LEADERBOARD)
    elif reac == '👎':
        LEADERBOARD[ppl[bot]] -= 1
        updateLeaderboards(f'{LOCAL_PATH}leaderboards.json', LEADERBOARD)


# Post the current leaderboard in chat, goes through bot list and puts an emoji representing
# the user to the left of their score.
@client.command()
async def leaderboards(ctx):
    global LEADERBOARD
    sort_LEADERBOARD = sorted(LEADERBOARD.items(), key=lambda x:x[1], reverse=True)

    msg = '__**BOT ROYALE LEADERBOARD**__:\n'
    for key, val in sort_LEADERBOARD:
        msg += f'{key}              `{val}`    \n'
        msg += f'------------------\n'

    msg = msg.replace('NAME', 'emoji_id') #emoji_id format is similar to <:emojiname:0123456789>
    await ctx.send(msg)


# This is the basic structure to setup a new markov bot
@client.command()
async def ace(ctx):
    sentences = sentenceHelpers.makeSentences(bots['botName']['model'], 200, 4)
    msg = randomSentence(sentences, 0, 12)
    await ctx.send(msg)


# posts the emoji of the requested user and calls the imgflip api to make a meme
# out of their markov'd text
@client.command()
async def meme(ctx):
    msss = ctx.message.content
    targ = msss.split('-meme ', 1)[1]

    sentences = sentenceHelpers.makeSentences(bots[targ]['model'], 200, 5)
    msg = randomSentence(sentences, 0, 10)

    msg_split = msg.split('> ', 1)
    user = msg_split[0] + '>'
    msg = msg_split[1]
    
    url = user + " " + memer.makeMeme(msg)
    await ctx.send(url)


@client.command()
async def helpme(ctx):
    msg = '''Help list
    ```
-helpme: display help list
-leaderboards: show current bot royale score```
    '''
    await ctx.send(msg)


client.run(BOT_TOKEN)