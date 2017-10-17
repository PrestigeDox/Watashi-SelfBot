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
        
        self.default_cogs = ('cogs.base', 'ignore')
        
        super().__init__(command_prefix=self.configs['prefix'], self_bot=True) 

        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)

    def run(self):
        super().run(self.configs['token'], bot=False)

    async def on_ready(self):
            print("Welcome to Watashi SelfBot!")
            print("Using this bot is against the Discord TOS.")
            print("Use at your own risk")
            for cog in self.default_cogs:
                self.load_extension(cog)