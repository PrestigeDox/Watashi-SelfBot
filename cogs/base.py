import discord
from discord.ext import commands

class Base:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True, aliases=['pingpong'])
	async def ping(self, ctx):
		await ctx.message.delete()
		pingtime = self.bot.latency * 1000
		pingtimerounded = int(pingtime)
		totalstring = str(pingtimerounded) + 'ms'
		emb = discord.Embed(title='Pong ' + totalstring, colour=0xC500FF)
		await ctx.send(embed=emb)
		

def setup(bot):
	bot.add_cog(Base(bot))