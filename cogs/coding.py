import discord
from discord.ext import commands
import unicodedata


class Coding:
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.user_color

    @commands.command(aliases=['python'])
    async def py(self, ctx, *, code: str):
        """Send Code In A Python Block"""
        await ctx.message.delete()
        await ctx.send("```py\n{}```".format(code))

    @commands.command()
    async def css(self, ctx, *, code: str):
        """Send Code In A CSS Block"""
        await ctx.message.delete()
        await ctx.send("```css\n{}```".format(code))

    @commands.command(aliases=['html5'])
    async def html(self, ctx, *, code: str):
        """Send Code In A HTML Block"""
        await ctx.message.delete()
        await ctx.send("```html\n{}```".format(code))

    @commands.command()
    async def ini(self, ctx, *, code: str):
        """Send Code In A INI Block"""
        await ctx.message.delete()
        await ctx.send("```ini\n{}```".format(code))

    @commands.command()
    async def c(self, ctx, *, code: str):
        """Send Code In A C Block"""
        await ctx.message.delete()
        await ctx.send("```c\n{}```".format(code))

    @commands.command()
    async def codeblock(self, ctx, *, code: str):
        """Send Text In A Code Block"""
        await ctx.message.delete()
        await ctx.send("```\n{}```".format(code))

    @commands.command(aliases=['onecodeblock'])
    async def linecodeblock(self, ctx, *, code: str):
        """Send Text In A Basic Code Block"""
        await ctx.message.delete()
        await ctx.send("``\n{}```".format(code))

    @commands.command()
    async def charinfo(self, ctx, char: str):
        """Get The CharInfo For Any Emoji"""
        await ctx.message.delete()

        digit = f'{ord(char):x}'
        name = unicodedata.name(char, 'Name not found.')

        emb = discord.Embed(colour=self.color)
        emb.set_author(name="Charinfo For {}".format(char))
        emb.add_field(name="Name", value=name, inline=False)
        emb.add_field(name="Char", value=f'\\U{digit:>08}', inline=False)
        emb.add_field(
            name="Link", value=f'<http://www.fileformat.info/info/unicode/char/{digit}>')
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Coding(bot))
