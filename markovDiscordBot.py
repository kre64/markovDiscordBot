import discord
import markovify
import random
import json
import sentenceHelpers
import memeImg
import threading
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


bots = {
    'ace': {
        'path': f'{LOCAL_PATH}rawtxt/ace_RAW.txt',
        'model': None
    },
    'prisn': {
        'path': f'{LOCAL_PATH}rawtxt/prisn_RAW.txt',
        'model': None
    },
    'pure': {
        'path': f'{LOCAL_PATH}rawtxt/pure_RAW.txt',
        'model': None
    },
    'falcon': {
        'path': f'{LOCAL_PATH}rawtxt/falcon_RAW.txt',
        'model': None
    },
    'poop': {
        'path': f'{LOCAL_PATH}rawtxt/MoJo_RAW.txt',
        'model': None
    },
    'sam': {
        'path': f'{LOCAL_PATH}rawtxt/allison_RAW.txt',
        'model': None
    },
    'bwin': {
        'path': f'{LOCAL_PATH}rawtxt/bwin_RAW.txt',
        'model': None
    },
    'boyd': {
        'path': f'{LOCAL_PATH}rawtxt/Secret_RAW.txt',
        'model': None
    },
    'melv': {
        'path': f'{LOCAL_PATH}rawtxt/natnap_RAW.txt',
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

# For updating markov raw data with markov generated data
def updateLake(path, data):
    with open(path, 'a') as f:
        f.write(f'\n{data}')


def updateLeaderboards(path, leaderboards):
    with open(path, 'w') as updated_leaderboards:
        json.dump(leaderboards, updated_leaderboards)

    print('Leaderboards have been updated')


# To update the bots data models every minute
def updateModels():
    threading.Timer(300.0, updateModels).start()
    for i, bot in bots.items():
        bot['model'] = makeModel(bot['path'])

    print('all bots updated')


def randomSentence(sentences, min_range, max_range):
    randnum = random.randint(min_range, max_range)
    return sentences[randnum][0]


@tasks.loop(seconds=10)
async def randomPost():
    channel = client.get_channel(706429703422083153)

    randnum = random.randint(0, len(bot_idx) - 1)
    bot = bot_idx[randnum]


    sentences = sentenceHelpers.makeSentences(bots[bot]['model'], 200, 4)
    msg = randomSentence(sentences, 0, 10)

    # updateLake(bots[bot]['path'], msg)

    new_interval = random.randint(3, 8)
    randomPost.change_interval(minutes=new_interval)
    print(f'new interval is: {new_interval}')
    await channel.send(msg)



@client.event
async def on_ready():
    updateModels()
    randomPost.start()
    print('Bot is ready.')


@client.event
async def on_reaction_add(reaction, user):
    # lazy implementation
    global LEADERBOARD
    ppl = {
        'ace': 'ace',
        'moe': 'prisn',
        'candler': 'falcon',
        'joe': 'pure',
        'peepoConnor': 'poop',
        'burp': 'sam',
        'babyyoda': 'bwin',
        'boydWeird': 'boyd',
        'megamelv': 'melv'

    }
    reac = reaction.emoji
    bot = reaction.message.content.split(':')[1]

    if reac == '👍':
        LEADERBOARD[ppl[bot]] += 1
        updateLeaderboards(f'{LOCAL_PATH}leaderboards.json', LEADERBOARD)
    elif reac == '👎':
        LEADERBOARD[ppl[bot]] -= 1
        updateLeaderboards(f'{LOCAL_PATH}leaderboards.json', LEADERBOARD)


@client.command()
async def leaderboards(ctx):
    global LEADERBOARD
    sort_LEADERBOARD = sorted(LEADERBOARD.items(), key=lambda x:x[1], reverse=True)

    msg = '__**BOT ROYALE LEADERBOARD**__:\n'
    for key, val in sort_LEADERBOARD:
        msg += f'{key}              `{val}`    \n'
        msg += f'------------------\n'

    msg = msg.replace('ace', '<:ace:458454740079083530>')
    msg = msg.replace('falcon', '<:candler:380992803754344448>')
    msg = msg.replace('pure', '<:joe:230148575907151872>')
    msg = msg.replace('prisn', '<:moe:412117049754648588>')
    msg = msg.replace('poop', '<:peepoConnor:585615852460703781>')
    msg = msg.replace('sam', '<:burp:252566045510991872>')
    msg = msg.replace('bwin', '<:babyyoda:647995987637436437>')
    msg = msg.replace('boyd', '<:boydWeird:541138309632753665>')
    msg = msg.replace('melv', '<:megamelv:585615889945329664>')
    await ctx.send(msg)


@client.command()
async def ace(ctx):
    sentences = sentenceHelpers.makeSentences(bots['ace']['model'], 200, 4)
    msg = randomSentence(sentences, 0, 50)

    # updateLake(bots['ace']['path'], msg)
    await ctx.send(msg)


@client.command()
async def prisn(ctx):
    sentences = sentenceHelpers.makeSentences(bots['prisn']['model'], 400, 4)
    msg = randomSentence(sentences, 0, 12)

    # updateLake(bots['prisn']['path'], msg)
    await ctx.send(msg)


@client.command()
async def pure(ctx):
    sentences = sentenceHelpers.makeSentences(bots['pure']['model'], 300, 4)
    msg = randomSentence(sentences, 0, 12)

    # updateLake(bots['pure']['path'], msg)
    await ctx.send(msg)


@client.command()
async def falcon(ctx):
    sentences = sentenceHelpers.makeSentences(bots['falcon']['model'], 200, 4)
    msg = randomSentence(sentences, 0, 12)

    # updateLake(bots['falcon']['path'], msg)
    await ctx.send(msg)


@client.command()
async def poop(ctx):
    sentences = sentenceHelpers.makeSentences(bots['poop']['model'], 200, 4)
    msg = randomSentence(sentences, 2, 6)

    # updateLake(bots['poop']['path'], msg)
    await ctx.send(msg)

@client.command()
async def sam(ctx):
    sentences = sentenceHelpers.makeSentences(bots['sam']['model'], 200, 4)
    msg = randomSentence(sentences, 0, 12)

    # updateLake(bots['sam']['path'], msg)
    await ctx.send(msg)

@client.command()
async def bwin(ctx):
    sentences = sentenceHelpers.makeSentences(bots['bwin']['model'], 200, 4)
    msg = randomSentence(sentences, 0, 12)

    # updateLake(bots['bwin']['path'], msg)
    await ctx.send(msg)

@client.command()
async def boyd(ctx):
    sentences = sentenceHelpers.makeSentences(bots['boyd']['model'], 200, 4)
    msg = randomSentence(sentences, 0, 12)

    # updateLake(bots['boyd']['path'], msg)
    await ctx.send(msg)

@client.command()
async def melv(ctx):
    sentences = sentenceHelpers.makeSentences(bots['melv']['model'], 200, 4)
    msg = randomSentence(sentences, 0, 12)

    # updateLake(bots['melv']['path'], msg)
    await ctx.send(msg)

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
-sam: summon sam bot
-bwin: summon bwin bot
-melv: summon melv bot
-boyd: summon boyd bot
-poop: summon mojo bot
-pure: summon joe bot
-prisn: summon prisn bot
-falcon: summon candler bot
-richard: summon richard bot
-leaderboards: show current bot royale score```
    '''
    await ctx.send(msg)

client.run(BOT_TOKEN)
