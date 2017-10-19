import discord
from discord.ext import commands
# import asyncio
import json
# import io
# import random
# import time
# import random
import aiohttp
from collections import namedtuple


class Watashi(commands.Bot):
    def __init__(self, config_path: str, *args, **kwargs):
        self.config_path = config_path
        with open(self.config_path) as f:
            self.configs = json.load(f)

        self.default_cogs = ('cogs.base', 'cogs.coding', 'cogs.emoji', 'cogs.wiki',
                             'cogs.aesthetic', 'cogs.urband', 'cogs.info',
                             'cogs.figlet', 'cogs.eval')

        self.embed_colour = int(self.configs['embed_colour'], 16)

        super().__init__(command_prefix=self.configs['prefix'], self_bot=True)
        self.color_tuple = namedtuple('Colors', 'red orange yellow darkgreen lightgreen lightblue darkblue blurple pruple grey')
        self.colors = Colors(0xff0000,
                           0xffa500,
                           0xffff00,
                           0x6400,
                           0x8ff00,
                           0xe5ff,
                           0xff,
                           0x7289da,
                           0x800080,
                           0x808080)

        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)

    def run(self):
        super().run(self.configs['token'], bot=False)

    async def on_ready(self):
        print("<----------------->\nWatashi SelfBot\n<----------------->\nCoded by:\nPrestige#9162\nDemo#9465\nnaught0#4417\n<----------------->\nWarning:\nUnder the MIT\nlicense we are\nnot liable for any\ndamage caused/\naction taken\nagainst you for\nusing a selfbot\nwhich is in violation\nof Discord's TOS")
        for cog in self.default_cogs:
            self.load_extension(cog)
