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
		emb = discord.Embed(title='Pong ' + totalstring, colour=self.bot.embed_colour)
		await ctx.send(embed=emb)
	
	@commands.command(hidden=True, aliases=['emb'])
	async def embed(self, ctx, *, message: str = None):
		if message == None:
			await ctx.message.delete()
			await ctx.send(":x: You need a message to embed")
		else:
			emb = discord.Embed(title=message, colour=self.bot.embed_colour)
			await ctx.send(embed=emb)

def setup(bot):
	bot.add_cog(Base(bot))