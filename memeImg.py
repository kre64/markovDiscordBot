import requests
import random
import json
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()

GET_MEMES_URL = os.getenv('GET_MEMES_URL')
MEMES_USERNAME = os.getenv('MEMES_USERNAME')
MEMES_PASS = os.getenv('MEMES_PASS')

# r = requests.get(url=GET_MEMES_URL)

# if r.status_code == 200:
# 	print(r.json())



class MemeImgs():
	def __init__(self):
		self.get_url = 'https://api.imgflip.com/get_memes'
		self.caption_url = 'https://api.imgflip.com/caption_image'
		self.template_ids = []

	def setTemplates(self):
		r = requests.get(url=self.get_url)
		bleh = []
		if r.status_code == 200:
			memes = r.json()['data']['memes']
			
			for meme in memes:
				self.template_ids.append(meme['id'])

	def requestRandom(self, top_text, bottom_text):
		randnum = random.randint(0, len(self.template_ids) - 1)

		data = {
			'template_id': self.template_ids[randnum],
			'username': MEMES_USERNAME,
			'password': MEMES_PASS,
			'text0': top_text,
			'text1': bottom_text,
		}

		r = requests.post(url=self.caption_url, data=data)
		img = r.json()['data']['url']

		return img

	# Cuts sentence in half for top, bottom text of the meme
	def makeMeme(self, sentence):
		words = sentence.split()
		word_count = len(words)

		first = int(word_count/2)

		top_text = ""
		bot_text = ""

		for x in range(0, first):
			top_text += " " + words[x]

		for x in range(first, word_count):
			bot_text += " " + words[x]

		url = self.requestRandom(top_text, bot_text)

		return url
			

# Example init
# memer = MemeImgs()
# memer.setTemplates()