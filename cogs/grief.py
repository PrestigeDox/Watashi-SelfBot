'''
Griefing on a server can lead to a ban.
When you get banned via using this cog
the owners of this bot are not liable
under the MIT licese. It may lead to
the disabling of your account.
'''

import discord
from discord.ext import commands

class Grief:
	def __init__(self, bot):
		self.bot = bot

	

def setup(bot):
	bot.add_cog(Base(bot))