import discord
import random
import gpt_2_simple as gpt2
import os

from discord.ext import commands, tasks
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

LOCAL_PATH = os.getenv('LOCAL_PATH')
data = f'{LOCAL_PATH}ace_RAWDAT.txt'

gpt2.download_gpt2(model_name='124M')
sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              dataset=data,
              model_name='124M',
              steps=1000
              )

bot_dir = LOCAL_PATH
gen_file = bot_dir + 'gpt2_gentext_{:%Y%m%d_%H%M%S}.txt'.format(datetime.utcnow())
gpt2.generate_to_file(sess,
                      destination_path=gen_file,
                      length=200,
                      temperature=1.0,
                      top_p=0.9,
                      prefix='<|startoftext|>',
                      truncate='<|endoftext|>',
                      include_prefix=False,
                      nsamples=1000,
                      batch_size=20
                      )
