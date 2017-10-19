import discord
from discord.ext import commands


class Coding:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['python'])
    async def py(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```py\n{}```".format(code))

    @commands.command()
    async def css(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```css\n{}```".format(code))

    @commands.command(aliases=['html5'])
    async def html(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```html\n{}```".format(code))

    @commands.command()
    async def ini(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```ini\n{}```".format(code))


    @commands.command()
    async def c(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```c\n{}```".format(code))

    @commands.command()
    async def codeblock(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("```\n{}```".format(code))

    @commands.command(aliases=['onecodeblock'])
    async def linecodeblock(self, ctx, *, code: str):
        await ctx.message.delete()
        await ctx.send("``\n{}```".format(code))


def setup(bot):
    bot.add_cog(Coding(bot))
