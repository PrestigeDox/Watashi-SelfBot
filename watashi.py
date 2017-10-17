import discord
from discord.ext import commands
# import asyncio
import json
# import io
# import random
# import time
# import random
import aiohttp


class Watashi(commands.Bot):
    def __init__(self, config_path: str, *args, **kwargs):
        self.config_path = config_path
        with open(self.config_path) as f:
            self.configs = json.load(f)
        
        self.default_cogs = ('cogs.base', 'cogs.coding')
        
        self.embed_colour = int(self.configs['embed_colour'], 16)

        super().__init__(command_prefix=self.configs['prefix'], self_bot=True) 

        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)

    def run(self):
        super().run(self.configs['token'], bot=False)

    async def on_ready(self):
            print('\n'*100)
            print("<----------------->\nWatashi SelfBot\n<----------------->\nCoded by:\nPrestige#9162\nDemo#9465\nnaught0#4417\n<----------------->\nWarning:\nUnder the MIT\nlisense we are\nnot liable for any\ndamage casued/\naction taken\nagainst you for\nusing a selfbot\nwhich is in violation\nof Discord's TOS")
            for cog in self.default_cogs:
                self.load_extension(cog)