import unicodedata
import discord
from discord.ext import commands


class Coding:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color

    @commands.command(aliases=['python'])
    async def py(self, ctx, *, code: str):
        """ Send Code In A Python Block """
        await ctx.message.edit(content="```py\n{}```".format(code))

    @commands.command()
    async def css(self, ctx, *, code: str):
        """ Send Code In A CSS Block """
        await ctx.message.edit(content="```css\n{}```".format(code))

    @commands.command(aliases=['html5'])
    async def html(self, ctx, *, code: str):
        """ Send Code In A HTML Block """
        await ctx.message.edit(content="```html\n{}```".format(code))

    @commands.command()
    async def ini(self, ctx, *, code: str):
        """ Send Code In A INI Block """
        await ctx.message.edit(content="```ini\n{}```".format(code))

    @commands.command()
    async def c(self, ctx, *, code: str):
        """ Send Code In A C Block """
        await ctx.message.edit(content="```c\n{}```".format(code))

    @commands.command()
    async def codeblock(self, ctx, *, code: str):
        """ Send Text In A Code Block """
        await ctx.message.edit(content="```\n{}```".format(code))

    @commands.command(aliases=['onecodeblock'])
    async def linecodeblock(self, ctx, *, code: str):
        """ Send Text In A Basic Code Block """
        await ctx.message.edit(content="```\n{}```".format(code))

    @commands.command()
    async def charinfo(self, ctx, char: str):
        """ Get The CharInfo For Any Emoji """
        digit = f'{ord(char):x}'
        name = unicodedata.name(char, 'Name not found.')

        await ctx.message.edit(content=
                               f'`\\U{digit:>08}` - {name} - <http://www.fileformat.info/info/unicode/char/{digit}>1')


def setup(bot):
    bot.add_cog(Coding(bot))
