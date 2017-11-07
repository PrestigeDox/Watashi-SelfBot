import discord
from discord.ext import commands


class Emoji:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color

    @commands.group(invoke_without_command=True)
    async def emoji(self, ctx):
        """ Shows the usage of the Emoji Command """
        emb = discord.Embed(colour=self.color)
        emb.add_field(name='Usage', value=f'```{self.bot.command_prefix}emoji <emojiname>```')
        await ctx.message.edit(embed=emb)

    @emoji.command()
    async def shrug(self, ctx):
        """ Lenny Shrug """
        await ctx.message.edit(content="¯\_(ツ)_/¯")

    @emoji.command()
    async def face(self, ctx):
        """ Lenny Face """
        await ctx.message.edit(content="( ͡° ͜ʖ ͡°)")

    @emoji.command()
    async def badman(self, ctx):
        """ Lenny Badman With Guns """
        await ctx.message.edit(content="̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з= ( ▀ ͜͞ʖ▀) =ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿")

    @emoji.command(aliases=['guns'])
    async def gun(self, ctx):
        """ Gun Emoji"""
        await ctx.message.edit(content="▄︻̷̿┻̿═━一")

    @emoji.command()
    async def ameno(self, ctx):
        """ Lenny Give Emoji """
        await ctx.message.edit(content="༼ つ ◕_◕ ༽つ")

    @emoji.command()
    async def sunglasses(self, ctx):
        """ Lenny Wearing Sunglasses """
        await ctx.message.edit(content="(▀̿Ĺ̯▀̿ ̿)")

    @emoji.command()
    async def eyesworried(self, ctx):
        """ Worried Eyes Emoji """
        await ctx.message.edit(content="ಠ_ಠ")

    @emoji.command(aliases=['5dollars', '5dollar', 'money'])
    async def fivedollar(self, ctx):
        """ Five Dollar Bill Emoji """
        await ctx.message.edit(content="[̲̅$̲̅(̲̅5̲̅)̲̅$̲̅]")

    @emoji.command()
    async def hiding(self, ctx):
        """  Hiding Lenny Man """
        await ctx.message.edit(content="┬┴┬┴┤ ͜ʖ ͡°) ├┬┴┬┴")

    @emoji.command()
    async def boxing(self, ctx):
        """ Boxing Emoji """
        await ctx.message.edit(content="(ง'̀-'́)ง")

    @emoji.command()
    async def tableflip(self, ctx):
        """ Lenny Table Flip """
        await ctx.message.edit(content="(╯°□°）╯︵ ┻━┻")

    @emoji.command(aliases=['0.o', '0.0', 'o.o'])
    async def weirdeyes(self, ctx):
        """ Weird Eyes Emoji """
        await ctx.message.edit(content="◉_◉")

    @emoji.command()
    async def tableflip2(self, ctx):
        """ Lenny Flipping 2 Tables at once """
        await ctx.message.edit(content="┻━┻ ︵ヽ(`Д´)ﾉ︵ ┻━┻")

    @emoji.command(aliases=['cuteface'])
    async def cute(self, ctx):
        """ Cute Face Emoji """
        await ctx.message.edit(content="(｡◕‿◕｡)")

    @emoji.command()
    async def unflip(self, ctx):
        """ Lenny Unflip """
        await ctx.message.edit(content="┬─┬﻿ ノ( ゜-゜ノ)")


def setup(bot):
    bot.add_cog(Emoji(bot))
