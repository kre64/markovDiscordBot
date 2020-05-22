import csv
import sys
import os

# Discord id can be found in discord dev mode

user = 'discord#discordId'
out_file = f"{LOCAL_PATH}rawtxt/{user.split('#')[0]}_RAW.txt"

# Bots need to print out emojis in this structure <:emojiName:emojiId> otherwise it's plaintext
# this replaces plaintext with the right emojiId
def customEmoji(text):
    emojis = {
        ':emojiName:': '<:emojiName:emojiId>',
    }

    new_text = text

    # replace emojis, and get rid of @everyone ping.
    for emoji in emojis:
        if emoji in text:
            new_text = new_text.replace(emoji, emojis[emoji])
        if '@everyone' in text:
            text.replace('@everyone', '')
    return new_text

# Replaces the discord#id from a sentence with an emoji that represents them
def userEmoji(user):
    user_emojis = {
        'discord#id': '<:emoji:id>',
    }

    if user in user_emojis:
        return user_emojis[user]
    
    return ''

with open(f'{LOCAL_PATH}csvfiles/rawData.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')

    # csv structure
    # ['AuthorID', 'Author', 'Date', 'Content', 'Attachments', 'Reactions']
    with open(out_file, 'w') as txt_file:
        for row in csv_reader:
            if row[1] == user and row[3] != '' and 'https' not in row[3]:
                text = sanitizeText(row[3])
                txt_file.write(f'{userEmoji(user)} {text}\n')


