import discord
import wikipedia
from discord.ext import commands

class Wiki:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True,pass_context=True)
	async def wiki(self, ctx, *, query: str):
		await ctx.message.delete()
		try:
			resultlst = await self.bot.loop.run_in_executor(None, wikipedia.search, query)
			item = resultlst[0]
			pg = await self.bot.loop.run_in_executor(None, wikipedia.page, item)
		except wikipedia.exceptions.DisambiguationError as e:
			pg = await self.bot.loop.run_in_executor(None, wikipedia.page, e.options[0])
		await ctx.send(pg.url)

	@wiki.command(pass_context=True,aliases=['-s'])
	async def search(self, ctx, *, query: str):
		await ctx.message.delete()
		resultlst = await self.bot.loop.run_in_executor(None, wikipedia.search, query)

		msg = str()
		for number, option in enumerate(resultlst[:4]):
			msg += "{0***REMOVED***. {1***REMOVED***\n".format(number+1, option)
		em = discord.Embed(title="Results",description=msg,color=self.bot.embed_colour)
		em.set_footer(text="Type 'exit' to leave the menu")
		menumsg = await ctx.send(embed=em)

		def check(m):
			return m.author == ctx.message.author and m.channel == ctx.message.channel and m.content.isdigit()
		response = await self.bot.wait_for('message',check=check)

		try:
			if response.content.lower() == 'exit':
				await response.delete()
				await menumsg.delete()
				return
			else:
				await response.delete()
				await menumsg.delete()
				item = resultlst[int(response.content)-1]
		except IndexError:
			return
		pg = await self.bot.loop.run_in_executor(None, wikipedia.page, item)
		await ctx.send(pg.url)
def setup(bot):
	bot.add_cog(Wiki(bot))