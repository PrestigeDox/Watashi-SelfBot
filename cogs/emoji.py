import discord
from discord.ext import commands

class Emoji:
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True)
	async def emoji(self, ctx):
		await ctx.message.delete()
		emb = discord.Embed(colour=self.bot.gold)
		emb.add_field(name='Usage', value='{***REMOVED***emoji <emojiname>'.format(self.bot.configs['prefix']))
		await ctx.send(embed=emb)

	@emoji.command()
	async def shrug(self, ctx):
		await ctx.message.delete()
		await ctx.send("¯\_(ツ)_/¯")

	@emoji.command()
	async def face(self, ctx):
		await ctx.message.delete()
		await ctx.send("( ͡° ͜ʖ ͡°)")

	@emoji.command()
	async def badman(self, ctx):
		await ctx.message.delete()
		await ctx.send("̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з= ( ▀ ͜͞ʖ▀) =ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿")

	@emoji.command(aliases=['guns'])
	async def gun(self, ctx):
		await ctx.message.delete()
		await ctx.send("▄︻̷̿┻̿═━一")

	@emoji.command()
	async def ameno(self, ctx):
		await ctx.message.delete()
		await ctx.send("༼ つ ◕_◕ ༽つ")

	@emoji.command()
	async def sunglasses(self, ctx):
		await ctx.message.delete()
		await ctx.send("(▀̿Ĺ̯▀̿ ̿)")

	@emoji.command()
	async def eyesworried(self, ctx):
		await ctx.message.delete()
		await ctx.send("ಠ_ಠ")

	@emoji.command(aliases=['5dollars', '5dollar', 'money'])
	async def fivedollar(self, ctx):
		await ctx.message.delete()
		await ctx.send("[̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]")

	@emoji.command()
	async def hiding(self, ctx):
		await ctx.message.delete()
		await ctx.send("┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴")

	@emoji.command()
	async def boxing(self, ctx):
		await ctx.message.delete()
		await ctx.send("(ง'̀-'́)ง")

	@emoji.command()
	async def tableflip(self, ctx):
		await ctx.message.delete()
		await ctx.send("(╯°□°）╯︵ ┻━┻")

	@emoji.command(aliases=['0.o', '0.0', 'o.o'])
	async def wierdeyes(self, ctx):
		await ctx.message.delete()
		await ctx.send("◉_◉")

	@emoji.command()
	async def tableflip2(self, ctx):
		await ctx.message.delete()
		await ctx.send("┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻")

	@emoji.command(aliases=['cuteface'])
	async def cute(self, ctx):
		await ctx.message.delete()
		await ctx.send("(｡◕‿◕｡)")

	@emoji.command()
	async def unflip(self, ctx):
		await ctx.message.delete()
		await ctx.send("┬─┬﻿ ノ( ゜-゜ノ)")

def setup(bot):
	bot.add_cog(Emoji(bot))