# markovDiscordBot  
Discord chat bot that outputs text from specific users using markov chains via markovify.

Also outputs markov text as image memes thanks to https://imgflip.com/

# Features  
*  Pretty realistic depictions of your discord pals
*  Leaderboards
*  Image memes
  
  
# Getting started
## Installation

1. Clone this repo into a destination of your choosing.
2. This is a discord bot, so you'll need to head on over to https://discord.com/developers/applications and set up a bot.
3. Head over [here](https://github.com/Tyrrrz/DiscordChatExporter "DiscordChatExporter") to download DiscordChatExporter, extract all the chats as **.csv** you want your bot to have memory of.
4. Install any missing pip requirements.
  - requests
  - random
  - json
  - discord
  - markovify
5. If you wish to use the [imgflip](https://imgflip.com/ "https://imgflip.com/") api, sign up for an account.
6. Setup a .env file with all of your relevant credentials and paths.
7. Create a leaderboards.json file with the botNames and a score of 0.
  ```JSON
  {
    "bot": 0, 
    "bot": 0, 
    "bot": 0, 
  }
  ```
8. Read through the code and fill in any generic data I've left behind for you.  
9. Let me know if I'm missing anything or make a PR :)

## Usage
python3 markovDiscordBot.py
# Screenshots  
![Basic usage](https://raw.githubusercontent.com/kre64/markovDiscordBot/master/Discord_HVd3NqVdhQ.png?token=AJJOBFBR4ZGWSRWN5LPO4ZK6ZBKDK "Basic usage")  
![Image meme](https://raw.githubusercontent.com/kre64/markovDiscordBot/master/Discord_ZdQcJLBgQc.png?token=AJJOBFEP7B4W4LKUMH6MDKS6ZBKBM "Image meme")  
![Leaderboard](https://raw.githubusercontent.com/kre64/markovDiscordBot/master/Discord_yAGT5lHxPt.png?token=AJJOBFD6MNQGWGGMPFU3LBC6ZBJ6M "Leaderboard")
