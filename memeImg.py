import requests
import json
import os

from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()

GET_MEMES_URL = os.getenv('GET_MEMES_URL')
MEMES_USERNAME = os.getenv('MEMES_USERNAME')

r = requests.get(url=GET_MEMES_URL)

if r.status_code == 200:
	print(r.json())

def init():


class MemeImgs():
	def __init__(self):
		self.get_url = 'https://api.imgflip.com/get_memes'
		self.caption_url = 'https://api.imgflip.com/caption_image'
		self.username = ''
		self.password = ''


	def request(template_id, top_text, bottom_text)