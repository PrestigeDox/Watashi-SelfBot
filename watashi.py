import discord
from discord.ext import commands
import asyncio
import json
import io
import random
import time
import random
import aiohttp

serverPrefix = {}

basecogs = ('cogs.base')
#Prefix not yet setup. Make config file.
bot = commands.Bot(command_prefix=, self_bot=True)
bot.aio_session = aiohttp.ClientSession(loop=bot.loop)

@bot.event
async def on_ready():
	print("Bot Online!")
	print("Name: {}".format(bot.user.name))
	print("ID: {}".format(bot.user.id))
	print(discord.__version__)
	for x in basecogs:
		bot.load_extension(x)

bot.run("", bot=False)
