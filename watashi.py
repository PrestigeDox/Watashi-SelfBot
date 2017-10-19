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

        self.default_cogs = ('cogs.base', 'cogs.coding', 'cogs.emoji', 'cogs.wiki',
                             'cogs.aesthetic', 'cogs.urband', 'cogs.info',
                             'cogs.figlet')

        self.embed_colour = int(self.configs['embed_colour'], 16)

        super().__init__(command_prefix=self.configs['prefix'], self_bot=True)

        # Colours
        self.gold = 16766720
        self.red = 16711680
        self.orange = 16753920
        self.yellow = 16776960
        self.darkgreen = 25600
        self.lightgreen = 589568
        self.lightblue = 58879
        self.darkblue = 255
        self.blurple = 7506394
        self.purple = 8388736
        self.grey = 8421504

        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)

    def run(self):
        super().run(self.configs['token'], bot=False)

    async def on_ready(self):
        print('\n' * 100)
        print("<----------------->\nWatashi SelfBot\n<----------------->\nCoded by:\nPrestige#9162\nDemo#9465\nnaught0#4417\n<----------------->\nWarning:\nUnder the MIT\nlicense we are\nnot liable for any\ndamage caused/\naction taken\nagainst you for\nusing a selfbot\nwhich is in violation\nof Discord's TOS")
        for cog in self.default_cogs:
            self.load_extension(cog)
