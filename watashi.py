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

        self.aiohttp_session = aiohttp.ClientSession(loop=self.loop)

        self.default_cogs = ('cogs.base')

        super().__init__(command_prefix=configs['prefix'], self_bot=True) 

    async def run(self):
        super().run(configs['bot_token'], bot=False)

    async def on_ready(self):
    	print('Bot Online!')
    	print(f'Name: {bot.user.name}')
    	print(f'ID: {bot.user.id}')
    	print(f'Discord.py Version: {discord.__version__}')

    	for cog in self.default_cogs:
    		bot.load_extension(cog)
