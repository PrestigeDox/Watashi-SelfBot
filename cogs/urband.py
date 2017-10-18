import discord
import urbandictionary as ud
from discord.ext import commands
class UrbanD:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True,pass_context=True,aliases=['ud','urbandict'])
	async def urban(self, ctx, *, query: str):
		await ctx.message.delete()
		try:
			resultlst = ud.define(query)
			item = resultlst[0]
		except:
			return
		await ctx.send('**{0***REMOVED*****:\n\n{1***REMOVED***\n\n**Examples**:\n\n{2***REMOVED***'.format(item.word,item.definition,item.example))
	@urban.command(pass_context=True,aliases=['-s'])
	async def search(self, ctx, *, query: str):
		await ctx.message.delete()
		resultlst = ud.define(query)
		msg = "```py\n"
		for number, option in enumerate(resultlst[:4]):
			msg += "{0***REMOVED***. {1***REMOVED***\n".format(number+1, option.word)
		msg += "\n\nType 'exit' to leave the menu\n```"
		menumsg = await ctx.send(msg)
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
		await ctx.send('**{0***REMOVED*****:\n\n{1***REMOVED***\n\n**Examples**:\n\n{2***REMOVED***'.format(item.word,item.definition,item.example))
	@urban.command(pass_context=True,aliases=['-r'])
	async def random(self, ctx):
		await ctx.message.delete()
		item = ud.random()[0]
		await ctx.send('**{0***REMOVED*****:\n\n{1***REMOVED***\n\n**Examples**:\n\n{2***REMOVED***'.format(item.word,item.definition,item.example))
def setup(bot):
	bot.add_cog(UrbanD(bot))