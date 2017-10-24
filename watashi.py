import discord
from discord.ext import commands
# import asyncio
import json
# import io
# import random
import datetime
# import random
import aiohttp
from collections import namedtuple
from formatter import EmbedHelp


class Watashi(commands.Bot):
    def __init__(self, config_path: str, *args, **kwargs):
        self.config_path = config_path
        with open(self.config_path) as f:
            self.configs = json.load(f)

        self.default_cogs = ('cogs.base', 'cogs.coding', 'cogs.emoji', 'cogs.wiki',
                             'cogs.aesthetic', 'cogs.urband', 'cogs.info', 'cogs.figlet', 
                             'cogs.eval', 'cogs.tinyurl', 'cogs.tags', 'cogs.games', 
                             'cogs.clean','cogs.error', 'cogs.define', 'cogs.purge',
                             'cogs.help','cogs.new_yt','cogs.elements', 'cogs.translate',
                             'cogs.animate')

        self.embed_colour = int(self.configs['embed_colour'], 16)

        super().__init__(command_prefix=self.configs['prefix'], self_bot=True)
        self.remove_command("help")
        self.formatter = EmbedHelp()

        # What even is this part?
        self.color_tuple = namedtuple('Colors', 'red orange yellow darkgreen lightgreen lightblue darkblue blurple purple grey')

        self.colors = self.color_tuple(0xff0000,
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
        print("<----------------->\n"
              "Watashi SelfBot\n"
              "<----------------->\n"
              "Coded by:\nPrestige#9162\nDemo#9465\nnaught0#4417\n"
              "<----------------->\n"
              "Warning:\n"
              "Under the MIT license, the makers of Watashi-SelfBot are not liable for any\n"
              "damage caused/action taken against you for using a selfbot, which is in violation of Discord's TOS")

        for cog in self.default_cogs:
            self.load_extension(cog)

        self.starttime = datetime.datetime.now()
